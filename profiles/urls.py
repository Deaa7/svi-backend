from django.urls import path
from . import views

urlpatterns = [
     path('get_teacher_preview/', views.get_teacher_preview), 
     path('get_teacher_info/<int:id>/', views.get_teacher_info), 
     path('update_teacher_profile/<int:id>/', views.UpdateTeacherProfile.as_view()), 
     path('get_student_own_profile_info/<int:id>/', views.get_student_own_profile_info), 
     path('update_student_profile/<int:id>/', views.UpdateStudentProfile.as_view()), 
     
     # Check if student has sufficient balance
     path('check_student_balance/', views.check_student_balance, name='check_student_balance'),
     
     path('increase_number_of_teacher_exams/<int:id>/', views.increase_number_of_teacher_exams),
     path('decrease_number_of_teacher_exams/<int:id>/', views.decrease_number_of_teacher_exams),
     path('increase_number_of_teacher_notes/<int:id>/', views.increase_number_of_teacher_notes),
     path('decrease_number_of_teacher_notes/<int:id>/', views.decrease_number_of_teacher_notes),
     
     
]