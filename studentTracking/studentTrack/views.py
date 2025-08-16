from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth import get_user_model
from django.http import HttpResponse
# Create your views here.

User=get_user_model()

def index(request):
    return render(request,'index.html')

def userLogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        print('username:',username)
        print('password:',password)
        print('user:',user)
        if user is not None:
            login(request,user)
            currentUser=User.objects.get(username=user.username)
            if currentUser.role=='student':
                return redirect('studentPage')
            elif currentUser.role=='teacher':
                return redirect('teacherPage')
            elif currentUser.is_staff:
                return redirect('adminPage')
    return render(request,'userLogin.html')
            
def adminPage(request):
    user=User.objects.get(pk=request.user.id).role
    if request.method=='GET' and user=='admin':
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
    return redirect('userLogin')
def editClasses(request):
    return render(request, 'editClasses.html')

def editSubjects(request):
    return render(request,'editSubject.html')

def studentSignup(request):
    if request.method=='GET':
        studentForm=StudentSignupForm()
        return render(request,'studentSignup.html',{'form':studentForm})
    if request.method=='POST':
        user=User.objects.get(id=request.POST.get('user'))
        subjects=request.POST.getlist('subjects')
        classroom=Classroom.objects.get(id=request.POST.get('classroom'))
        dateOfBirth=request.POST.get('dateOfBirth')
        guardian=request.POST.get('guardian')
        student,created=Student.objects.get_or_create(
            user=user,classroom=classroom,dateOfBirth=dateOfBirth,guardian=guardian
            )
        if student or created:
            student.subjects.set(subjects)
            student.save()
        print(student)
        student.save()
        form = StudentSignupForm(request.POST)
        """
        if form.is_valid():
            user=form.save(commit=False)
            form.save_m2m()
            user.role='student'
            user.save()"""
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
        form=CreateUser(request.POST)
        if form.is_valid:
            user=form.save(commit=False)
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
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
    #Show a visualization of learners vs their averages in that subject
    #Show a peformance graph for classroom vs average for that classroom to compare 
    #performance across classrooms
    user=User.objects.get(pk=request.user.id).role
    if request.method=='GET' and user=='teacher':
        subject=Subject.objects.get(pk=pk)
        students=Student.objects.filter(subjects=subject)
        assignmentId=request.POST.get('id')
        AssignmentInstance=None
        try:
            AssignmentInstance=Assignment.objects.get(subject__id=pk)
            assignmentAmnt=AssignmentInstance.assignmentAmnt
        except Assignment.DoesNotExist:
            pass
        form=createAssignmentForm(request.POST,instance=AssignmentInstance)
        if form.is_valid():
            assignment=form.save(commit=False)
        
            assignmentSubject=Subject.objects.get(name=assignment)
            assignmentAmnt=request.POST['assignmentAmnt']
            assignmentWeight=request.POST['assignmentWeight']
            finalTestWeight=request.POST['finalTestWeight']
            term=request.POST['term']
        
            studentAssignmentSettings,created=Assignment.objects.get_or_create(
                subject=assignmentSubject,term=term
            )
        
            studentAssignmentSettings.assignmentAmnt=assignmentAmnt
            studentAssignmentSettings.assignmentWeight=assignmentWeight
            studentAssignmentSettings.finalTestWeight=finalTestWeight
            studentAssignmentSettings.save()
            #assignment.subject=subject
            #assignment.save()
            #form.save()
            numberOfAssignments=list(range(int(assignmentAmnt)))
            #numberOfAssignments=list(range(1,assignment.assignmentAmnt+1))
        else:
            form=createAssignmentForm()
            numberOfAssignments=list(range(int(assignmentAmnt)))
    
    #Create visualizations
    '''
    try:
        marks=StudentMark.objects.filter(subject=subject)
        data=marks.values_list('learner__username','average')
        learners,averages=zip(*data)
        plt.bar(learners,averages)
        plt.xlabel('Learner')
        plt.ylabel('Average')
        plt.title('Learner Averages')
    
        buffer=BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png=buffer.getvalue()
        buffer.close()
        plt.close()
    
        graphic=base64.b64decode(image_png).decode('utf-8')
    except:
        graphic=None
        '''
    try:
        return render(request,'teacherSubject.html',{'students':students,'subject':subject,'form':form,'number':numberOfAssignments})
    except:
        return redirect('userLogin')

    
def addMarks(request,subject_id,user_id):
    #Get or create the student assignment/ their overall scores for the subject
    studentSubject=Subject.objects.get(id=subject_id)
    learner=User.objects.get(id=user_id)
    studentMarks,created=StudentMark.objects.get_or_create(learner=learner,subject=studentSubject)
    
    marks=[]
    courseWorkMarkWights=0
    finalMark=0
    courseWork=0
    amountOfAssignments=-1
    for i in request.POST:
        try:
            i=int(request.POST[i])
            marks.append(i)
        except:
            continue
    assignment=Assignment.objects.get(subject=subject_id)
    distrib=MarksDistribution.objects.get(assignment=assignment)
    courseWorkMarkWights=distrib.distribution
    for i in range(len(marks)-1):
        amountOfAssignments=i
        courseWork=courseWork+marks[i]
        finalMark=finalMark+(marks[i]/100*courseWorkMarkWights[i])
        print(finalMark)
    examMarkWeight=assignment.finalTestWeight
    courseMark=courseWork/amountOfAssignments
    average=finalMark+(examMarkWeight*(marks[-1]/100))
    examMark=marks[-1]
    
    #create the StudentMark for students with calculated values
    
    studentMarks.courseMark=courseMark
    studentMarks.ExamMark=examMark
    studentMarks.average=average
    studentMarks.save()
    '''
    subject=Subject.objects.get(pk=subject_id)
    courseMarks=0
    testMarks=request.POST.get_list('Mark_'+ user_id)
    marksAmnt=len(testMarks)
    for mark in testMarks:
        courseMarks+=int(mark)
    courseMarks=courseMarks/marksAmnt
    finalTestMark=int(request.POST.get('FinalTest_'+user_id))
    
    #Get the assignment weighs and the final test weigh
    #Get assignment for that subject
    assignment=Assignment.objects.get(subject=subject)
    #get assignmentWeight and finalTestWeight
    assWeight=assignment.assignmentWeight
    assFinal=assignment.finalTestWeight
    
    #Calculate average
    coursePercentage=assWeight * courseMarks
    examPercentage=assFinal * finalTestMark
    finalPercentage=examPercentage + coursePercentage
    
    studentMark,created=StudentMark.objects.update_or_create(learner=request.user,subject=subject,courseMark=courseMarks,ExamMark=finalTestMark,average=finalPercentage)
    studentMark.save()
    '''
    return redirect('teacherPage')

def studentSubjectDetails(request,pk):
    subject=Subject.objects.get(pk=pk)
    try:
        marks=StudentMark.objects.get(subject=subject,learner=request.user)
    except StudentMark.DoesNotExist:
        marks=None
    return render(request,'studentSubjectDetails.html',{'marks':marks,'subject':subject.name})

def addMarkDistribution(request):
    markDistribution=[]
    for i in request.POST:
        try:
            markDistribution.append(int(request.POST[i]))
        except ValueError:
            continue
        
    assignment=Assignment.objects.get(subject=request.POST.get('subject'))
    distribution,created=MarksDistribution.objects.get_or_create(assignment=assignment)
    distribution.distribution=markDistribution
    distribution.save()
    return HttpResponse("Mark distribution successfully added")
              
       
                

                
        
        
    