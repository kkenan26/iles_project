from django.rest_framework import serializers
from .models import CustomUser, InternshipPlacement, WeeklyLog, Evaluation, EvaluationCriteria

class CustomUserSerializer(serializers.ModelSerializers):
    class Meta:
        model = CustomUser
        fields = '__all__'