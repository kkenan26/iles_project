from rest_framework import serializers
from .models import CustomUser, InternshipPlacement, WeeklyLog, Evaluation, EvaluationCriteria

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','first_name','last_name','role','phone_number']

class InternshipPlacementSerializer(serializers.ModelSerializer):
    student_name =serializers.CharField(source= 'student.username', read_only = True)
    worplace_supervisor_name= serializers.CharField(source='workplace_supervisor.username', raed_only= True)
    academic_supervisor_name=serializers.CharField(source= 'academic_supervisor.username', read_only= True)

    class Meta:
        model = InternshipPlacement
        fields ='__all__'
        read_only_fields= ['created_at']

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("Start Date cannot be after end date")
        return data

class WeeklyLogSerializer(serializers.ModelSerializer):
   

    class Meta:
        model=WeeklyLog
        fields ='__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    criteria_name= serializers.CharField(source= 'criteria.name',read_only=True)
    student_name= serializers.CharField(source= 'student.username', read_only=True)
    evaluator_name =serializers.CharField(source= 'evaluator.username, read_only=True')
    criteria_weight=serializers.DecimalField(source='criteria.weight', max_digits=5, decimal_paces=2, read_only=True)

    class Meta:
        model= Evaluation
        fields= '__all__'
        read_only_fields= ['evaluator','evaluauted_at']

    def validate(self, value):
        if  value< 0 or value >100:
            raise serializers.ValidationError("Score must be between 0and 100")
        return value

class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model =EvaluationCriteria
        fields= ['id', 'name','description','weight','is_active']