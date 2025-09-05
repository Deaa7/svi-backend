from django.contrib import admin
from .models import DoneExams

# Register your models here.


 
   
class DoneExamsAdmin(admin.ModelAdmin):
    
    list_display = ['student','subject_name','date_of_application','exam_name','exam_id','result' ]
    search_fields = ['student']
    list_filter = ['student']   
   



#  pass
admin.site.register(DoneExams , DoneExamsAdmin)