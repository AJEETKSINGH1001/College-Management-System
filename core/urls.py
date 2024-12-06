from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('student_admission/', views.student_admission, name='student_admission'),
    path('student_profiles/', views.student_profiles, name='student_profiles'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    #path('record_attendance/', views.record_attendance, name='record_attendance'),
    #path('view_attendance/', views.view_attendance, name='view_attendance'),
    #path('student-id-card/<int:student_id>/', views.student_id_card, name='student_id_card'),
    path('student-id-card-pdf/<int:student_id>/', views.student_id_card_pdf, name='student_id_card_pdf'),
    path('student-dashboard/pay_fee/', views.pay_fee, name='pay_fee'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.add_faculty, name='add_faculty'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('faculty/<int:pk>/edit/', views.edit_faculty, name='edit_faculty'),
    path('faculty/<int:pk>/delete/', views.delete_faculty, name='delete_faculty'),
]

# Serve media files during development (only for local development, not in production)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
