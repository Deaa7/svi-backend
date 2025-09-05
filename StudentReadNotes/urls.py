from django.urls import path
from . import views

urlpatterns = [
    # Create a new StudentReadNotes instance
    path('create/', views.create_student_read_note, name='create_student_read_note'),
    
    # Increase number of reads for a specific instance
    path('increase_reads/<int:id>/', views.increase_number_of_reads, name='increase_number_of_reads'),
    
    # Get read notes for a specific student with pagination
    path('get_read_notes/<int:student_id>/', views.get_read_notes, name='get_read_notes'),
    
    # Generic CRUD views
    path('list_create/', views.StudentReadNotesListCreateView.as_view(), name='student_read_notes_list_create'),
]
