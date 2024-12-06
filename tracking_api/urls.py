from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_package/', views.add_package, name='add_package'),
    path('package_history/<str:tracking_number>/', views.package_history, name='package_history'),
    path('package_status/<str:tracking_number>/', views.package_status, name='package_status'),
    
]

