from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request,'index.html')

def userLogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            currentUser=CustomUser.objects.get(username=user.username)
            if currentUser.role=='student':
                return redirect('studentPage')
            elif currentUser.role=='teacher':
                return redirect('teacherPage')
            elif currentUser.is_staff:
                return redirect('adminPage')
    return render(request,'userLogin.html')
            
def adminPage(request):
    if request.method=='GET':
        #Get all classrroms and subjects
        classrooms=Classroom.objects.all()
        subjects=Subject.objects.all()
        roleForm = SelectRoleForm()
        createUserForm=CreateUser()
        
        return render(request, 'adminPage.html',{
            'userForm':createUserForm,
            'form':roleForm,
            'classes':classrooms,
            "subjects":subjects,
            })
        
    if request.method=='POST':
        roleForm = SelectRoleForm(request.POST)
        if roleForm.is_valid():
            role= roleForm.cleaned_data['user_type']
            if 'student' in role:
                return redirect('studentSignup')
            elif 'teacher' in role:
                return redirect('teacherSignup')
                
def editClasses(request):
    return render(request, 'editClasses.html')

def editSubjects(request):
    return render(request,'editSubject.html')

def studentSignup(request):
    if request.method=='GET':
        studentForm=StudentSignupForm()
        return render(request,'studentSignup.html',{'form':studentForm})
    if request.method=='POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.role='student'
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request,'studentSignup.html',{'form':form})

def teacherSignup(request):
    if request.method=='GET':
        teacherForm=TeacherSignUpForm()
        return render(request,'teacherSignup.html',{'form':teacherForm})
    if request.method=='POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.role='teacher'
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request,'teacherSignup.html',{'form':form})
        
def deleteSubject(request, pk):
    subject=Subject.objects.get(pk=pk)
    subject.delete()
    return redirect('adminPage')

def addSubject(request):
    form=createSubjectForm()
    if request.method=='GET':
        return render(request,'addSubject.html',{'form':form})
    if request.method=='POST':
        form=createSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
        
        

def viewClassroom(request, pk):
    #Get all students from the class with specified pk arguement
    classroom=Classroom.objects.get(pk=pk)
    students=Student.objects.filter(classroom=classroom)
    return render(request,'classroomView.html',{'students':students})


def createClassroom(request):
    if request.method=="GET":
        form=createClassroomForm()
        return render(request,'createClassroom.html',{'form':form})
    if request.method=="POST":
        form=createClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
            

def deleteClassroom(request,pk):
    Classroom.objects.get(pk=pk).delete()
    return redirect('adminPage')

def createUser(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('adminPage')
        return redirect('adminPage')
            
def studentView(request,pk):
    #Get all marks specifically for the student with provided pk
    stdnt=CustomUser.objects.get(pk=pk)
    marks=StudentMark.objects.filter(learner=stdnt)
    return render(request,'studentView.html',{'marks':marks}) 

def subjectView(request,pk):
    subject=Subject.objects.get(pk=pk) 
    students=Student.objects.all()
    stds=students.filter(subjects=subject)
    return render(request,'subjectView.html',{'students':stds})

def studentPage(request):
    student=Student.objects.get(user=request.user)
    studentSubjects=student.subjects.all()
    Subject.objects.filter
    return render(request,'studentPage.html',{'subjects':studentSubjects,'name':request.user})

def teacherPage(request):
    teacher=Teacher.objects.get(user=request.user)
    subs=Subject.objects.filter(educator=teacher)
    return render(request,'teacherPage.html',{'subjects':subs})

def teacherSubject(request,pk):
    subject=Subject.objects.get(pk=pk)
    students=Student.objects.filter(subjects__pk=pk)
    assignmentId=request.POST.get('id')
    AssignmentInstance=None
    try:
        AssignmentInstance=Assignment.objects.get(subject=subject)
    except Assignment.DoesNotExist:
        pass
    form=createAssignmentForm(request.POST,instance=AssignmentInstance)
    if form.is_valid():
        assignment=form.save(commit=False)
        assignment.subject=subject
        assignment.save()
        numberOfAssignments=list(range(1,assignment.assignmentAmnt+1))
    else:
        form=createAssignmentForm()
        numberOfAssignments=[1]
        
    return render(request,'teacherSubject.html',{'students':students,'subject':subject,'form':form,'number':numberOfAssignments})
    
def addMarks(request,subject_id,user_id):
    pass

def studentSubjectDetails(request,pk):
    subject=Subject.objects.get(pk=pk)
    try:
        marks=StudentMark.objects.get(subject=subject,learner=request.user)
    except StudentMark.DoesNotExist:
        marks=None
    return render(request,'studentSubjectDetails.html',{'marks':marks,'subject':subject.name})
              
       
                

                
        
        
    