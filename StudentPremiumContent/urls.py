from django.urls import path
from . import views

urlpatterns = [
    # Main endpoint to get premium content by student ID with pagination
    path('student/<int:student_id>/', views.get_premium_content_by_student, name='get_premium_content_by_student'),
    
    # Get premium content details by ID
    path('details/<int:id>/', views.get_premium_content_details, name='get_premium_content_details'),
    
    
    # Create new premium content record
    # path('create/', views.create_premium_content, name='create_premium_content'),
    
    # Create premium content with balance check and deduction
    path('create-with-balance-check/', views.create_premium_content_with_balance_check, name='create_premium_content_with_balance_check'),
    
    # Check if student has premium access to specific content
    path('check-access/<int:student_id>/<int:content_id>/<str:content_type>/', views.check_premium_access, name='check_premium_access'),
    
    # Check if student has purchased specific content by type and ID
    path('check-purchase/', views.check_content_purchase, name='check_content_purchase'),
    
    # Generic views for CRUD operations
    path('', views.StudentPremiumContentListCreateView.as_view(), name='premium_content_list_create'),
    path('<int:pk>/', views.StudentPremiumContentDetailView.as_view(), name='premium_content_detail'),
]
