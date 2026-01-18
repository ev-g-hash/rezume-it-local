# resume/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
]