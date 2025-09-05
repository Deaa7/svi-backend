

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('all_questions/<int:package_id>/', views.get_all_questions),
    path('add_questions/', views.add_questions.as_view()),
    path('add_question_images/', views.AddQuestionImages.as_view()),
    path('get_question_images/<int:test_id>/', views.get_question_images),
    path('edit_question_by_id/<int:id>/', views.edit_question_by_id),
    path('delete_question_by_id/<int:id>/', views.delete_question_by_id),
]
