from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-demo-users/', views.create_demo_users, name='create_demo_users'),
    path('superadmin/add_admin/', views.add_admin, name='add_admin'),
    path('superadmin/view_admins/', views.view_admins, name='view_admins'),
    path('admin/add_mentor/', views.add_mentor, name='add_mentor'),
    path('admin/view_mentors/', views.view_mentors, name='view_mentors'),
]
