from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin): 
    list_display = ['username','email','is_teacher','number_of_login_sessions' ,'is_staff','date_joined']
    search_fields = ['username']
    list_filter = ['username']   
   

admin.site.register(User,UserAdmin)