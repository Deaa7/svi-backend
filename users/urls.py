from django.contrib import admin
from django.urls import path  , include, reverse_lazy
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('register/',views.register , name='register'),
  path('login/',views.login , name='login'),
  path('logout/',views.LogoutView.as_view() , name='logout'),
  path('refresh/', views.TokenRefreshViewCustom.as_view(), name='token_refresh'),

]