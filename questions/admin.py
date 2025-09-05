from django.contrib import admin
 
from questions.models import Questions , QuestionImages
# Register your models here.
 
 
class QuestionsAdmin(admin.ModelAdmin):
  list_display=['package','test_content']
  list_filter=['test_content']
  autocomplete_fields=['package']
  
admin.site.register(Questions ,QuestionsAdmin)
admin.site.register(QuestionImages)
