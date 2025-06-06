from . import views
from django.urls import path

urlpatterns = [
    #admin related paths
    path('', views.index, name='index'),
    path('createUser',views.createUser,name='createUser'),
    path('userLogin',views.userLogin,name='userLogin'),
    path('adminPage',views.adminPage,name='adminPage'),
    path('editClasses',views.editClasses,name='editClasses'),
    path('editSubjects', views.editSubjects,name='editSubjects'),
    path('studentSignup', views.studentSignup,name='studentSignup'),
    path('teacherSignup', views.teacherSignup,name='teacherSignup'),
    path('deleteSubject/<int:pk>',views.deleteSubject,name='deleteSubject'),
    path('addSubject',views.addSubject,name='addSubject'),
    path('viewClassroom/<int:pk>',views.viewClassroom,name='viewClassroom'),
    path('createClassroom',views.createClassroom,name='createClassroom'),
    path('deleteClassroom/<int:pk>',views.deleteClassroom,name='deleteClassroom'),
    path('studentView/<int:pk>',views.studentView,name='studentView'),
    path('subjectView<int:pk>',views.subjectView,name='subjectView'),
    #Teacher related paths
    path('teacherPage',views.teacherPage,name='teacherPage'),
    path('teacherSubject/<int:pk>',views.teacherSubject,name='teacherSubject'),
    #student related paths
    path('studentPage',views.studentPage,name='studentPage'),
    path('addMarks/<int:subject_id>/<int:user_id>/', views.addMarks, name='addMarks'),
    path('studentSubjectDetails/<int:pk>',views.studentSubjectDetails,name='studentSubjectDetails')

    
]
