from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import upload_students_csv

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
    path('class_scheduling/', views.class_scheduling, name='class_scheduling'),
    path('save_schedule/', views.save_schedule, name='save_schedule'),
    path('view_timetable/', views.view_timetable, name='view_timetable'),
    path('faculty/<int:faculty_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_form, name='add_course'),
    path('courses/<int:course_id>/edit/', views.course_form, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='delete_course'),
    path('courses/<int:course_id>/modules/', views.module_list, name='module_list'),
    path('courses/<int:course_id>/modules/add/', views.module_form, name='add_module'),
    path('courses/<int:course_id>/modules/<int:module_id>/edit/', views.module_form, name='edit_module'),
    path('courses/<int:course_id>/modules/<int:module_id>/delete/', views.module_delete, name='delete_module'),
    #path('courses/add/', views.course_form, name='add_course'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/add/', views.batch_add, name='batch_add'),
    path('batches/<int:batch_id>/edit/', views.batch_edit, name='batch_edit'),
    path('batches/<int:batch_id>/delete/', views.batch_delete, name='batch_delete'),
    path('student_details/', upload_students_csv, name='upload_students_csv'),
    path('download_sample_csv/', views.download_sample_csv, name='download_sample_csv'),
    path('search-students/', views.search_students, name='search_students'),
    path('schedule_exam/', views.schedule_exam, name='schedule_exam'),
    path('view_exams/', views.view_exams, name='view_exams'),
]


# Serve media files during development (only for local development, not in production)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
