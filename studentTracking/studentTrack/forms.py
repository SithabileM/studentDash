from django import forms
from .models import *

class TeacherSignUpForm(forms.ModelForm):
    class Meta:
        model= Teacher
        fields=('user','classroom')
        
class StudentSignupForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=('user','subjects','classroom','dateOfBirth','guardian')
        
        
class SelectRoleForm(forms.Form):
    user_type=forms.ChoiceField(choices=[('teacher','Teacher'),('student','Student')], widget=forms.RadioSelect)
    
class CreateUser(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('username','password','role')
        
class createClassroomForm(forms.ModelForm):
    class Meta:
        model=Classroom
        fields=('grade','room','year')
        
class createSubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields=('name','educator')
        
class createAssignmentForm(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=('assignmentAmnt','assignmentWeight','finalTestWeight','term')
    
    
        
    