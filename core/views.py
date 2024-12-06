from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import role_required
from .forms import StudentAdmissionForm, CustomUserRegistrationForm
from .models import Student
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image as PILImage
from django.contrib.auth.decorators import login_required
from .models import Student
from .decorators import role_required
from reportlab.lib import colors
from django.shortcuts import render, get_object_or_404, redirect
from .models import Faculty
from .forms import FacultyForm
from django.contrib.admin.views.decorators import staff_member_required

# Home page view
def home(request):
    return render(request, 'core/home.html')


# Admin Dashboard view
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')


# Faculty Dashboard view
@login_required
@role_required(['faculty'])
def faculty_dashboard(request):
    return render(request, 'core/faculty_dashboard.html')


# Student Dashboard view
@login_required
@role_required(['student'])
def student_dashboard(request):
    try:
        # Get the Student object associated with the logged-in user
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None
    return render(request, 'core/student_dashboard.html', {'student': student})


# Parent Dashboard view
@login_required
@role_required(['parent'])
def parent_dashboard(request):
    return render(request, 'core/parent_dashboard.html')


# Login view with role-based redirection
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Role-based redirection
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'faculty':
                return redirect('faculty_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'parent':
                return redirect('parent_dashboard')
            else:
                messages.error(request, "Your role is not recognized.")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('home')


# User registration view
def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "There was an error in the registration. Please try again.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


# Student admission form view
def student_admission(request):
    if request.method == 'POST':
        form = StudentAdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_profiles')
    else:
        form = StudentAdmissionForm()
    return render(request, 'student_admission.html', {'form': form})


# Student profiles list view
def student_profiles(request):
    students = Student.objects.all()
    return render(request, 'student_profiles.html', {'students': students})


# Individual student details view
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student_detail.html', {'student': student})


# Generate and display student ID card
# Generate ID card as PDF
@login_required
@role_required(['student'])
def student_id_card_pdf(request, student_id, user=None):
    student = get_object_or_404(Student, id=student_id)

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="id_card_{student.enrollment_number}.pdf"'

    # Create PDF buffer
    buffer = BytesIO()

    # Define card size (6x4 inches) in points (1 inch = 72 points)
    width, height = 432, 288  # 6 inches x 4 inches
    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    # Define layout properties
    margin = 20
    photo_width = 80
    photo_height = 80
    start_x = margin  # Start position for the photo
    start_y = height - margin - photo_height  # Start position for the photo

    # Add a colored rectangle as the background for the card
    pdf.setFillColor(colors.lightblue)  # Set a professional background color
    pdf.rect(margin, margin, width - 2 * margin, height - 2 * margin, fill=1)

    # Add Student Photo to the ID card (ensure photo exists and is accessible)
    try:
        student_photo_path = user.student_profile.profile_image
        student_image = PILImage.open(student_photo_path)
        student_image = student_image.resize((photo_width, photo_height), PILImage.ANTIALIAS)
        student_image_path = "/tmp/student_photo.jpg"
        student_image.save(student_image_path)  # Save the resized image temporarily

        # Draw the image on the PDF
        pdf.drawImage(student_image_path, start_x, start_y, width=photo_width, height=photo_height)
    except Exception as e:
        print(f"Error loading student photo: {e}")
        # If no photo, just add a placeholder image or skip the photo
        pdf.setFillColor(colors.grey)
        pdf.rect(start_x, start_y, photo_width, photo_height, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(start_x + 10, start_y + 30, "No Photo")  # Label for the placeholder

    # Add text details about the student
    text_start_x = start_x + photo_width + 10  # Space between photo and text
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(text_start_x, start_y + 60, f"Name: {student.first_name} {student.last_name}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(text_start_x, start_y + 45, f"Enrollment Number: {student.enrollment_number}")
    pdf.drawString(text_start_x, start_y + 30, f"Phone: {student.user.student_profile.phone_number}")
    pdf.drawString(text_start_x, start_y + 15, f"DOB: {student.user.student_profile.date_of_birth}")
    pdf.drawString(text_start_x, start_y, f"Address: {student.user.student_profile.address}")

    # Add College Principal's Name, Signature, and Stamp
    principal_name = "Dr. John Doe"  # Replace with actual Principal's name
    signature_path = "/path/to/signature.png"  # Replace with the actual path to the signature image
    stamp_path = "/media/student_documents/stamp.png"  # Replace with the actual path to the college stamp image

    # Add Principal's Name
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(220, 40, f"Principal: {principal_name}")

    # Add Principal's Signature (ensure the image exists and is accessible)
    try:
        pdf.drawImage(signature_path, 220, 10, width=60, height=30)
    except Exception as e:
        print(f"Error loading signature: {e}")
        # If no signature image, we can skip or add a placeholder
        pdf.setFont("Helvetica", 10)
        pdf.drawString(220, 10, "Signature Not Available")

    # Add College Stamp
    try:
        pdf.drawImage(stamp_path, 300, 10, width=60, height=60)
    except Exception as e:
        print(f"Error loading stamp: {e}")
        # If no stamp image, we can skip or add a placeholder
        pdf.setFont("Helvetica", 10)
        pdf.drawString(300, 10, "Stamp Not Available")

    # Finish up the PDF and send it to the response
    pdf.showPage()
    pdf.save()

    # Reset buffer position
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response


def pay_fee(request):
    return render(request, 'core/pay_fee.html')  # Ensure this points to your HTML file


@staff_member_required
def faculty_list(request):
    faculty_members = Faculty.objects.all()
    return render(request, 'faculty/faculty_list.html', {'faculty_members': faculty_members})

# Add a new faculty profile
def add_faculty(request):
    if request.method == "POST":
        form = FacultyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'faculty/add_faculty.html', {'form': form})

from core.forms import FacultyForm


class UpdateView:
    pass


def reverse_lazy(param):
    pass


class FacultyUpdateView(UpdateView):
    model = Faculty
    form_class = FacultyForm
    template_name = 'faculty_edit.html'
    success_url = reverse_lazy('faculty_list')  # Redirect after successful edit

# View a specific faculty profile
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty})


def edit_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, request.FILES, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty_detail', pk=faculty.pk)
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'faculty/faculty_edit.html', {'form': form, 'faculty': faculty})


from django.urls import reverse_lazy
from django.views.generic import DeleteView
from core.models import Faculty

class FacultyDeleteView(DeleteView):
    model = Faculty
    template_name = 'faculty_confirm_delete.html'
    success_url = reverse_lazy('faculty_list')  # Redirect after successful deletion


def delete_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        return redirect('faculty_list')
    return redirect('faculty_detail', pk=pk)