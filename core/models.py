from django.db import models
from django.contrib.auth.models import AbstractUser

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