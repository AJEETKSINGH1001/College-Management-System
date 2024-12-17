# core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from core.models import CustomUser, Student, Feedback, Courses, Module, Department, Marks
from django import forms
from .models import Faculty
#from .views import Batch


class LoginForm(AuthenticationForm):
    # Customizing the fields for better form UI
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )


class UserCreationForm:
    pass


class ValidationError(Exception):
    pass


def make_password(param):
    pass


#class User:


class CustomUserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('parent', 'Parent')])

    def save(self):
        cleaned_data = self.cleaned_data

        # Hash the password
        hashed_password = make_password(cleaned_data['password1'])

        # Create the user
        user = CustomUser.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=hashed_password,  # Save the hashed password
            role=cleaned_data['role']
        )
        return user

    from django import forms
    from .models import Student

    class StudentAdmissionForm(forms.ModelForm):
        class Meta:
            model = Student
            fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address', 'documents',
                      'fee_paid']
            widgets = {
                'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            }


class StudentAdmissionForm:
    def save(self):
        pass



class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'email', 'phone', 'qualification', 'experience', 'subjects_taught', 'profile_picture']
        widgets = {
            'subjects_taught': forms.Textarea(attrs={'rows': 3}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['faculty', 'rating', 'comments']
        widgets = {
            'faculty': forms.HiddenInput(),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ['name', 'code', 'credit_hours', 'department','duration_weeks',]
        department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course code'}),
            'credit_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter credit hours'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department or its sub section'}),
            'duration_weeks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter duration in weeks'}),

            # 'department': forms.Select(attrs={'class': 'form-control'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['courses', 'name', 'code', 'description', 'hours']


# core/forms.py

from django import forms
from .models import Batch

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'courses', 'semester', 'stream']

    courses = forms.ModelChoiceField(
        queryset=Courses.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a Course"  # Optional placeholder
    )


from django import forms

class StudentCSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")



from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_name', 'date', 'time', 'venue', 'course11', 'subjects', 'seating_arrangement']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'course', 'courses', 'exam', 'marks_obtained', 'total_marks']

        # Add widgets for better UI
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a student'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a course'
            }),
            'courses': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select courses'
            }),
            'exam': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select an exam'
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter marks obtained'
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total marks'
            }),
        }
        labels = {
            'student': 'Student Name',
            'course': 'Course',
            'courses': 'Courses',
            'exam': 'Exam',
            'marks_obtained': 'Marks Obtained',
            'total_marks': 'Total Marks',
        }


from django import forms

class MarksUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Please upload a valid CSV file.')
        return file


from django import forms
from .models import Course
from captcha.fields import CaptchaField

class ResultPublicationForm(forms.Form):
    roll_number = forms.CharField(max_length=50, label="Roll Number", widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'}))
    course1 = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course", widget=forms.Select(attrs={'class': 'form-control'}))
    captcha = CaptchaField()