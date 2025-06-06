from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.conf import settings
# Create your models here.
currectYear=datetime.datetime.now().year

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10,choices=[('teacher','Teacher'),('student','Student'),('admin','Admin')])
        
class Classroom(models.Model):
    grade= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(13)])
    room = models.CharField(max_length=1)
    year = models.IntegerField(validators=[MinValueValidator(1900),MaxValueValidator(currectYear)],default=currectYear)
    
    def __str__(self):
        return str(self.grade) + self.room
        
               
class Teacher(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    classroom = models.ManyToManyField(Classroom)
    
    
    def __str__(self):
        return self.user.username
    
class Subject(models.Model):
    name = models.CharField(max_length=30,unique=True)
    educator= models.OneToOneField(Teacher,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    subject=models.OneToOneField(Subject,on_delete=models.CASCADE)
    assignmentAmnt=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=1)
    assignmentWeight=models.FloatField(default=50)
    finalTestWeight=models.FloatField(default=50)
    term=models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(4)])
    
    def __str__(self):
        return self.subject.name
    
class Student(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    classroom = models.OneToOneField(Classroom, on_delete=models.CASCADE)
    dateOfBirth=models.DateField(null=True,blank=True)
    guardian=models.CharField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
class StudentMark(models.Model):
    learner=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    subject=models.OneToOneField(Subject,on_delete=models.CASCADE)
    courseMark=models.FloatField(default=0)
    ExamMark=models.FloatField(default=0)
    average=models.FloatField(default=0)
    
    def __str__(self):
        return self.learner.username + self.subject.name
    
    
    