from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(
        (None,{'fields':('role',)}),
    )
    
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(StudentMark)