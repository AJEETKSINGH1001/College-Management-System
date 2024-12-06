# core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

from core.models import CustomUser, Student
from django import forms
from .models import Faculty

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

