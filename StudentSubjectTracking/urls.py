from django.urls import path
from . import views

app_name = 'student_subject_tracking'

urlpatterns = [
    # Create subject tracking instance
    path('create/', views.StudentSubjectTrackingCreateView.as_view(), name='create-tracking'),
    
    # Retrieve all records by student and class
    path('student/<int:student_id>/class/<str:Class>/', views.StudentSubjectTrackingByStudentClassView.as_view(), name='get-by-student-class'),
    
    # Increase counts
]
