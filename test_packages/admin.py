from django.contrib import admin
from .models import TestPackage
from questions.models import Questions
from django.db import connection
from django.contrib.admin.models import LogEntry


# Register your models here.
class QuestionsInline(admin.StackedInline):
    model =Questions 
    extra = 0

 
class TestPackageAdmin(admin.ModelAdmin): 
    list_display = ['package_name','id','publisher_name','subject_name' ,'CLASS','publisher_id','number_of_questions','number_of_apps' , 'number_of_purchases','Price'   ]
    search_fields = ['package_name','subject_name','price' , 'publisher_name' , 'Class']
    list_filter =['package_name' ,'subject_name','price']   
    inlines = [QuestionsInline] 
   
    def CLASS(self, obj):
        return 'بكلوريا' if obj.Class == '12' else 'تاسع'
    
    def Price(self, obj):
        return 'مجاني' if obj.price == 0 else f'{obj.price} ل.س'
    
admin.site.register(TestPackage ,TestPackageAdmin)



class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        "action_time",
        "user",
        "object_repr",
        "action_flag",
        "change_message",
    ]
    readonly_fields = (
        "action_time",
        "user",
        "content_type",
        "object_repr",
        "action_flag",
        "change_message",
        "object_id",
    )

    list_filter = ("action_flag", "user")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False


admin.site.register(LogEntry, LogEntryAdmin)
