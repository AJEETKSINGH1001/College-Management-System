from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('register/', auth_views.LoginView.as_view(template_name='core/register.html'), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
