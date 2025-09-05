 
 
from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [ 
 path('examDoneRecord/',views.ExamDoneRecord.as_view()),
 path('student_done_exams/<int:id>/',views.get_exams_done_by_student_id ),
]
