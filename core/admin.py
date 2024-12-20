from django.contrib import admin
from .models import CustomUser, Student, Course1, Schedule, Courses, Module, StudentDetails, Exam, Marks, Results
from django.contrib.auth.admin import UserAdmin
from .models import Student
from .models import Faculty


#from .models import Batch


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active'),
        }),
    )

from django.contrib import admin
from .models import Batch

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'courses', 'semester', 'stream', 'created_at']
    list_filter = ['courses', 'semester', 'stream']
    search_fields = ['name', 'course__name']


# Register CustomUser model with the custom UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Faculty)
#admin.site.register(Attendance)
admin.site.register(Course1)
admin.site.register(Schedule)
admin.site.register(Courses)
admin.site.register(Module)
admin.site.register(StudentDetails)
#admin.site.register(Batch)
admin.site.register(Exam)
admin.site.register(Marks) #
admin.site.register(Results)


