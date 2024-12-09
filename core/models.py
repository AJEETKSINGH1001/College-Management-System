from django.contrib.auth.models import AbstractUser
from django.db import models

from CollegeManagementSystem import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_profile"  # Optional: makes reverse lookup easier
    )
    enrollment_number = models.CharField(max_length=15, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    documents = models.FileField(upload_to='student_documents/', blank=True, null=True)
    fee_paid = models.BooleanField(default=False)
    admission_date = models.DateField(auto_now_add=True)
    some_field = models.CharField(max_length=100, blank=True, null=True)  # Additional field
    profile_image = models.ImageField(upload_to='student_documents/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically set `some_field` based on `fee_paid`
        self.some_field = f"{self.fee_paid}" if self.fee_paid else "0.00"

        # Generate unique enrollment_number if not already set
        if not self.enrollment_number:
            self.enrollment_number = self.generate_enrollment_number()

        # Save the instance
        super().save(*args, **kwargs)

    def generate_enrollment_number(self):
        # Get the latest enrollment number and increment it
        last_student = Student.objects.order_by('id').last()
        if last_student and last_student.enrollment_number.startswith("EN"):
            numeric_part = int(last_student.enrollment_number[2:])
            new_numeric_part = numeric_part + 1
        else:
            new_numeric_part = 1  # Start from 1 if no student exists

        return f"EN{new_numeric_part:03d}"  # Format: EN001, EN002, etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.enrollment_number})"

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=200)
    # = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    subjects_taught = models.TextField(help_text="List of subjects taught")
    profile_picture = models.ImageField(upload_to='faculty_pictures/', blank=True, null=True)
    avg_rating = models.FloatField(default=0.0)


    def __str__(self):
        return self.name


class Course:
    objects = None


from core.models import Course  # Ensure the path is correct


class Course1(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

import datetime
class Schedule(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course1, on_delete=models.CASCADE)  # Link to Course
    schedule_date = models.DateField(default=datetime.date(2024, 1, 1))
    schedule_time = models.TimeField(default=datetime.time(9, 0))  # Default to 9:00 AM

    def __str__(self):
        return f"{self.faculty} - {self.course}"

from django.contrib.auth.models import User
class Feedback(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings 1-5
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])
    #comments = models.TextField()

    def __str__(self):
        return f"Feedback by {self.student} for {self.faculty} - {self.rating}"

class Performance(models.Model):
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Performance of {self.faculty.name}"


class Avg:
    pass


class Courses(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credit_hours = models.IntegerField()
    duration_weeks = models.IntegerField()
    department = models.CharField(max_length=100)  # Can be replaced with a ForeignKey to a Department model
    #duration_weeks = models.IntegerField()
    def __str__(self):
        return f"{self.name} ({self.code})"

class Department(models.Model):
     name = models.CharField(max_length=255)


class Module(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    hours = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.courses.name}"