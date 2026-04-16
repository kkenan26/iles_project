from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES=[
        ('student','Student Intern'),
        ('workplace_supervisor','Workplace Supervisor'),
        ('internship_admin','Internship Administrator'),
        ('academic_supervisor','Academic Supervisor')
    ]
    role = models.CharField(max_length=21, choices= ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank= True)

    def __str__(self):
        return f"{self.username}({self.role})"
    

class InternshipPlacement(models.Model):
    STATUS_CHOICES= [('pending','Pending'),
                      ('active','Active'), 
                      ('canceled', 'Canceled'),
                      ('completed','Completed')
                      ]

    student = models.ForeignKey(
        CustomUser, 
        on_delete = models.CASCADE,
        related_name='placements')

    workplace_supervisor = models.ForeignKey(
        CustomUser,
        on_delete= models.SET_NULL,
        null =True,
        related_name= 'supervised_placements')    
    
    academic_supervisor=models.ForeignKey(
        CustomUser,
        on_delete = models.SET_NULL,
        null = True,
        related_name= 'academic_placements')
    
    company_name = models.CharField(max_length= 200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,
                               choices= STATUS_CHOICES,
                               default = 'pending')
    
    def __str__(self):
        return f"{self.student.username}@{self.company_name}"
    
class WeeklyLog(models.Model):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('submitted','Submitted'),
        ('reviewed','Reviewed'),
        ('approved','Approved')
    ]

    placement = models.ForeignKey(InternshipPlacement,
                                  on_delete = models.CASCADE,
                                  related_name = 'weekly_logs'
                                  )
    
    week_number = models.PositiveIntegerField()
    activities = models.TextField()

    challenges = models.TextField(null= True, blank= True)
    skills_gained = models.TextField(null= True, blank = True)

    status = models.CharField(max_length=20,
                              choices = STATUS_CHOICES,
                              default= 'draft')
    
    submitted_at= models.DateTimeField(null= True, blank= True)
    created_at =models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together= ('placement','week_number')

    def __str__(self):
        return f"Week {self.week_number} - {self.placement.student.username}"

class EvaluationCriteria(models.Model):
    name =models.CharField(max_length= 100, unique=True)
    description =models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits= 5, decimal_places= 2)
    is_active=models.BooleanField(default= True)

    class Meta:
        verbose_name_plural= "Evaluation Criteria"
    def __str__(self):
        return f"{self.name}: {self.weight}"

class Evaluation(models.Model):
    placement= models.ForeignKey(InternshipPlacement,
    on_delete=models.CASCADE, related_name='evaluations')
    criteria= models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE, related_name='evaluated_criteria')
    evaluator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='student_evaluator')
    score=models.DecimalField(max_digits=5, decimal_places=2)
    comments= models.TextField(null =True, blank=True)
    evaluated_at= models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together= ('placement','criteria')

    def weighted_score(self):
        return (self.score * self.criteria.weight)/100

    def __str__(self):
        return f"{self.criteria}: {self.score}"    