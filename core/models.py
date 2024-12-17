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

# core/models.py

from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    # Other fields...

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="batches")
    semester = models.IntegerField()
    stream = models.CharField(max_length=100, blank=True, null=True)  # Optional stream
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.courses.name}"


from django.db import models

class StudentDetails(models.Model):
    enrollment_number = models.CharField(max_length=50, unique=True)
    roll_number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    course = models.CharField(max_length=100)
    subjects = models.TextField()  # Comma-separated subject names
    semester = models.IntegerField()
    batch = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.enrollment_number})"


class Exam(models.Model):
    exam_name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    course11 = models.ForeignKey('Course1', on_delete=models.CASCADE)
    subjects = models.ForeignKey('Courses', on_delete=models.CASCADE)
    seating_arrangement = models.TextField(blank=True, help_text="Details about seating arrangement")

    def __str__(self):
        return f"{self.exam_name} - {self.subjects.name} on {self.date}"


# New Marks Model
class Marks(models.Model):
    student = models.ForeignKey(StudentDetails,null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course1, on_delete=models.CASCADE)
    courses = models.ForeignKey(Courses,null=True, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100

    @property
    def gpa(self):
        """Simple GPA calculation (Assuming 10-point scale)."""
        return round((self.percentage / 10), 2)

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.exam.exam_name}"

    class Result(models.Model):
        roll_number = models.CharField(max_length=50)
        course = models.ForeignKey(Course1, on_delete=models.CASCADE)
        courses = models.CharField(max_length=100)
        marks_obtained = models.IntegerField()
        total_marks = models.IntegerField()
        gpa = models.FloatField()

        def __str__(self):
            return f"{self.course.name} - {self.roll_number}"