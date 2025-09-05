from django.contrib import admin
from .models import Profile_Student
from .models import Profile_Teacher
# Register your models here.

class ProfileStudentAdmin(admin.ModelAdmin):  # student 

    list_display = ['user' ,'full_name','city']
    search_fields = ['city']
    list_filter = ['city']


class ProfileTeacherAdmin(admin.ModelAdmin): # teacher
   list_display = ['user','full_name','studying_subjects','Class','total_net','phone_number','another_phone_number','city']
   search_fields = ['user','full_name','studying_subjects','Class','total_net','phone_number','another_phone_number','city']
   list_filter = ['user','full_name','studying_subjects','Class','total_net','phone_number','another_phone_number','city']

admin.site.register(Profile_Student  , ProfileStudentAdmin)
admin.site.register(Profile_Teacher , ProfileTeacherAdmin)
