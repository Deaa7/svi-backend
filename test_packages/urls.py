from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('testing_get_all', views.GetAllPackages)

urlpatterns = [
    path('get_packages/<str:subject_name>/', views.get_all_packages),
    path('get_student_solved_exams/<str:subject_name>/', views.get_student_solved_exams),
    path('get_single_package/<int:id>/', views.get_package_info   ),
    path('increase_num_of_apps/<int:id>/', views.increase_num_of_apps   ),
    path('increase_number_of_purchases/<int:id>/', views.increase_num_of_purchases   ),
    path('create_test_packages/', views.create_test_packages.as_view()   ),
    path('get_package_details/<int:id>/', views.get_package_details ),
  path('get_test_packages_by_publisher_id/<int:id>/' , views.get_packages_by_publisher),
    path('edit_test_package/<int:id>/', views.edit_test_package),
    path('delete_test_package/<int:id>/', views.delete_test_package),
]
