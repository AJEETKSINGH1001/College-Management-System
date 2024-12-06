from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def __str__(self):
        return self.name
