from django.contrib import admin
from .models import Notes , NoteImages

class NotesAdmin(admin.ModelAdmin): 
    list_display =  ['title' ,'publisher_name' , 'price','subject_name','Class','number_of_reads','number_of_purchases','number_of_comments']
    search_fields = ['title','publisher_name','subject_name','price']
    list_filter = ['title' ,'subject_name','price']   
 
   


admin.site.register(Notes , NotesAdmin  )
admin.site.register(NoteImages )