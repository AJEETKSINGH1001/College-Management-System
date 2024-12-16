from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models, apps
from .decorators import role_required
from .forms import StudentAdmissionForm, CustomUserRegistrationForm, CourseForm, ModuleForm
from .models import Student, Course1, Feedback, Module, Courses
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
from .models import Faculty, Course, Schedule

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


from django.core.paginator import Paginator
@login_required
def faculty_list(request):
    # Determine user role
    user_role = None
    if request.user.is_authenticated:
        if request.user.is_staff:  # Assuming staff means admin
            user_role = 'admin'
        elif request.user.groups.filter(name='Faculty').exists():
            user_role = 'faculty'
        else:
            user_role = 'student'

    # Filter faculty members by search query (if any)
    search_query = request.GET.get('search', '')
    faculty_members = Faculty.objects.all()
    if search_query:
        faculty_members = faculty_members.filter(
            name__icontains=search_query
        ) | faculty_members.filter(
            email__icontains=search_query
        )

    # Pagination
    paginator = Paginator(faculty_members, 10)  # Show 10 faculty members per page
    page_number = request.GET.get('page')
    faculty_members = paginator.get_page(page_number)

    # Render the template with all context
    return render(request, 'faculty/faculty_list.html', {
        'faculty_members': faculty_members,
        'search_query': search_query,
        'user_role': user_role,  # Pass user role for role-based logic in the template
    })
# Add a new faculty profile
@staff_member_required
@role_required(['admin'])
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
@staff_member_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    feedbacks = faculty.feedbacks.all()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'faculty/faculty_detail.html', {
        'faculty': faculty,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
    })

@staff_member_required
@role_required(['admin'])
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

@staff_member_required
@role_required(['admin'])
def delete_faculty(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        return redirect('faculty_list')
    return redirect('faculty_detail', pk=pk)


from .models import Faculty, Course
@staff_member_required
@role_required(['admin'])
def class_scheduling(request):
    # Fetch all faculty and courses
    faculty_members = Faculty.objects.all()
    courses = Course1.objects.all()

    return render(request, 'faculty/class_scheduling.html', {
        'faculty_members': faculty_members,
        'courses': courses
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Schedule
import datetime

@staff_member_required
@role_required(['admin'])
def save_schedule(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        course_id = request.POST.get('course')
        schedule_date = request.POST.get('schedule_date')  # Get schedule_date from the form
        schedule_time = request.POST.get('schedule_time')  # Get schedule_time from the form

        # Check if schedule_time is provided
        if not schedule_time:
            messages.error(request, "Schedule time is required.")
            return redirect('class_scheduling')

        # Parse the schedule_time to ensure it's in the correct format (HH:MM)
        try:
            # Ensure that schedule_time is parsed into a proper time object
            schedule_time = datetime.datetime.strptime(schedule_time, '%H:%M').time()
        except ValueError:
            messages.error(request, "Invalid time format. Please use the correct time format (HH:MM).")
            return redirect('class_scheduling')

        # Create a schedule entry
        try:
            Schedule.objects.create(
                faculty_id=faculty_id,
                course_id=course_id,
                schedule_date=schedule_date,  # Ensure schedule_date is also passed correctly
                schedule_time=schedule_time  # Save the time as a TimeField
            )
            messages.success(request, "Class schedule saved successfully!")
        except Exception as e:
            messages.error(request, f"Error saving schedule: {str(e)}")

        # After saving, redirect to timetable page to show the schedule
        return redirect('view_timetable')

    # views.py

    def view_timetable(request):
        # Fetch all the schedules
        schedules = Schedule.objects.all()

        # Filter by faculty if a faculty ID is provided
        faculty_id = request.GET.get('faculty')
        if faculty_id:
            schedules = schedules.filter(faculty_id=faculty_id)

        # Get all faculty members for the filter dropdown
        faculty_members = Faculty.objects.all()

        return render(request, 'faculty/view_timetable.html', {
            'schedules': schedules,
            'faculty_members': faculty_members,
            'selected_faculty_id': faculty_id  # Pass the selected faculty ID to maintain the filter state
        })


# views.py

def view_timetable(request):
    # Fetch all the schedules
    schedules = Schedule.objects.all()

    # Filter by faculty if a faculty ID is provided in the GET request
    faculty_id = request.GET.get('faculty')
    if faculty_id:
        schedules = schedules.filter(faculty_id=faculty_id)

    # Get all faculty members for the filter dropdown
    faculty_members = Faculty.objects.all()

    # Handle PDF generation if requested
    if 'export_pdf' in request.GET:
        # Create a buffer for the PDF
        buffer = BytesIO()

        # Create a PDF Canvas
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(220, 750, "Class Timetable")
        pdf.setFont("Helvetica", 12)

        # Set up column headers
        y = 700
        pdf.drawString(50, y, "Faculty")
        pdf.drawString(200, y, "Course")
        pdf.drawString(400, y, "Schedule")
        pdf.line(50, y - 10, 550, y - 10)  # Draw a line under headers
        y -= 30

        # Populate rows
        for schedule in schedules:
            pdf.drawString(50, y, schedule.faculty.name)
            pdf.drawString(200, y, schedule.course.name)
            pdf.drawString(400, y, schedule.schedule_time.strftime("%I:%M %p"))  # Format time properly
            y -= 20

            # Avoid writing beyond the page boundary
            if y < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = 750

        # Save and return the PDF response
        pdf.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="timetable.pdf"'
        return response

    # Render the HTML template
    return render(request, 'faculty/view_timetable.html', {
        'schedules': schedules,
        'faculty_members': faculty_members,
        'selected_faculty_id': faculty_id,  # Pass the selected faculty ID to maintain the filter state
    })


from django.db.models import Avg
from .models import Faculty, Feedback
from .forms import FeedbackForm

from django.db.models import Avg
from .models import Faculty, Feedback, Performance
from .forms import FeedbackForm

@login_required
def submit_feedback(request, faculty_id):
    # Get the faculty object (if not found, it will return a 404 error)
    faculty = get_object_or_404(Faculty, id=faculty_id)

    if request.method == 'POST':
        # Extract feedback data from the form
        rating = int(request.POST.get('rating'))
        comments = request.POST.get('comments')

        # Create a new feedback entry
        Feedback.objects.create(
            faculty=faculty,
            student=request.user,
            rating=rating,
            comments=comments
        )

        # Recalculate the average rating for the faculty
        feedbacks = Feedback.objects.filter(faculty=faculty)
        avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']

            # If the faculty does not have a performance, create a new performance record

        # Also update the average rating directly on the faculty model
        faculty.avg_rating = avg_rating if avg_rating else 0.0  # Ensure the field is not None
        faculty.save()

        # Redirect to the faculty list page after submission
        return redirect('faculty_list')  # Replace 'faculty_list' with the correct URL name if needed

    return render(request, 'faculty/submit_feedback.html', {'faculty': faculty})

from django.db.models import Avg
def update_performance(faculty_id):
    faculty = Faculty.objects.get(id=faculty_id)
    feedbacks = Feedback.objects.filter(faculty=faculty)
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0.0
    faculty.performance.average_rating = avg_rating
    faculty.performance.save()

def admin_performance_dashboard(request):
    faculties = Faculty.objects.all().select_related('performance')
    return render(request, 'admin/faculty_performance_dashboard.html', {'faculties': faculties})


# List all courses

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

@staff_member_required
def course_list(request):
    # Retrieve query parameters
    department = apps.get_model('core', 'Department')
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'name')  # Default sorting by name
    page_number = request.GET.get('page', 1)  # Default to the first page

    # Fetch all courses
    courses = Courses.objects.all()

    # Filter courses based on search query
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(department__name__icontains=search_query)  # Ensure department is a ForeignKey
        )

    # Validate and apply sorting
    valid_sort_fields = ['name', 'code', 'credit_hours', 'department__name']
    if sort_field in valid_sort_fields:
        courses = courses.order_by(sort_field)

    # Paginate courses (10 items per page)
    paginator = Paginator(courses, 10)
    courses_page = paginator.get_page(page_number)

    # Render the template with context
    return render(request, 'courses/course_list.html', {
        'courses': courses_page,
        'search_query': search_query,
        'sort_field': sort_field,
    })


# Add or edit a course
from .forms import CourseForm


from .forms import CourseForm
from .models import Courses
@staff_member_required
def course_form(request, course_id=None):
    # If the course_id is provided, fetch the course to edit
    if course_id:
        course = get_object_or_404(Courses, pk=course_id)  # Fetch the course by its ID
        form = CourseForm(request.POST or None, instance=course)  # Populate the form with existing data
    else:
        form = CourseForm(request.POST or None)  # If no course_id, create a new course form

    # Handling form submission
    if request.method == 'POST':
        if form.is_valid():
            form.save()  # Save the course (create or update)
            return redirect('course_list')  # Redirect to the course list page after saving

    return render(request, 'courses/course_form.html', {'form': form})

# Delete a course
@staff_member_required
def course_delete(request, course_id):
    # Get the course object by its ID or raise a 404 if it doesn't exist
    course = get_object_or_404(Courses, pk=course_id)  # Make sure 'Courses' is used, not 'Course'

    # Handle the DELETE request
    if request.method == 'POST':
        #course = get_object_or_404(Course, id=course_id)
        course.delete()  # Delete the course
        return redirect('course_list')  # Redirect to course list after deletion

    # Render confirmation page for course deletion (optional)
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# List modules of a course
@staff_member_required
def module_list(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    modules = course.modules.all()
    return render(request, 'courses/module_list.html', {'course': course, 'modules': modules})

# Add or edit a module
@staff_member_required

def module_form(request, course_id, module_id=None):
    course = get_object_or_404(Course, id=course_id)
    module = get_object_or_404(Module, id=module_id) if module_id else None
    form = ModuleForm(request.POST or None, instance=module)
    if form.is_valid():
        module = form.save(commit=False)
        module.course = course
        module.save()
        return redirect('module_list', course_id=course.id)
    return render(request, 'courses/module_form.html', {'form': form, 'course': course})

# Delete a module
@staff_member_required
def module_delete(request, course_id, module_id):
    module = get_object_or_404(Module, id=module_id)
    module.delete()
    return redirect('module_list', course_id=course_id)



# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Batch, Course
from .forms import BatchForm
@staff_member_required
def batch_list(request):
    batches = Batch.objects.all()
    paginator = Paginator(batches, 10)  # Show 10 batches per page

    page_number = request.GET.get('page')  # Get current page number from URL
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    return render(request, 'batches/batch_list.html', {'page_obj': page_obj})

from django.shortcuts import render, redirect
from .forms import BatchForm

@staff_member_required
def batch_add(request):
    if request.method == 'POST':
        form = BatchForm(request.POST)
        if form.is_valid():
            try:
                batch = form.save()  # Save the form without committing
                batch.courses = form.cleaned_data['courses']  # Explicitly set the course
                print(f"Debug: Batch before saving - {batch}")
                batch.save()  # Save the batch instance
                print("Batch saved successfully.")
                return redirect('batch_list')  # Redirect to batch list
            except Exception as e:
                print(f"Error during batch save: {e}")
        else:
            print("Form errors:", form.errors)  # Print form errors
    else:
        form = BatchForm()

    return render(request, 'batches/batch_form.html', {'form': form})

@staff_member_required
def batch_edit(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            return redirect('batch_list')
    else:
        form = BatchForm(instance=batch)

    return render(request, 'batches/batch_form.html', {'form': form})

@staff_member_required
def batch_delete(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    if request.method == 'POST':
        batch.delete()
        return redirect('batch_list')
    return render(request, 'batches/batch_confirm_delete.html', {'batch': batch})



import csv
from .forms import StudentCSVUploadForm
from .models import StudentDetails
@staff_member_required
def upload_students_csv(request):
    if request.method == "POST":
        form = StudentCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                for row in reader:
                    StudentDetails.objects.update_or_create(
                        enrollment_number=row['Enrollment Number'],
                        defaults={
                            'roll_number': row['Roll Number'],
                            'name': row['Name'],
                            'course': row['Course'],
                            'subjects': row['Subjects'],  # Assuming comma-separated
                            'semester': row['Semester'],
                            'batch': row['Batch'],
                        }
                    )
                messages.success(request, "Students data uploaded successfully!")
                return redirect('upload_students_csv')
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {e}")
    else:
        form = StudentCSVUploadForm()

    return render(request, 'student_details/upload_students_csv.html', {'form': form})

from django.http import HttpResponse
import os

@staff_member_required
def download_sample_csv(request):
    # Specify the absolute path to the sample CSV file
    sample_csv_path = os.path.join('core/templates/student_details/sample_students_upload.csv')  # Ensure 'sample.csv' exists in the static directory

    if os.path.exists(sample_csv_path):
        with open(sample_csv_path, 'r') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sample_students_upload.csv"'
            return response
    else:
        return HttpResponse("Sample CSV file not found.", status=404)

from django.shortcuts import render
from .models import StudentDetails
from django.db.models import Q

@staff_member_required
def search_students(request):
    query = None
    student = None

    if request.method == "GET":
        query = request.GET.get('query', None)
        if query:
            # Search for students by enrollment_number or roll_number
            student = StudentDetails.objects.filter(
                Q(enrollment_number__icontains=query) | Q(roll_number__icontains=query)
            ).first()  # Get the first match or None if no match

    return render(request, 'student_details/search_students.html', {'student': student, 'query': query})


from .models import Exam
from .forms import ExamForm
from django.contrib import messages

@login_required
@role_required(['admin'])
def schedule_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam scheduled successfully!")
            return redirect('view_exams')
    else:
        form = ExamForm()
    return render(request, 'exams/schedule_exam.html', {'form': form})


def view_exams(request):
    # Fetch all courses for the filter dropdown
    courses = Course1.objects.all()

    # Get the selected course from the query parameters
    selected_course_id = request.GET.get('course')

    # Filter exams by the selected course if provided
    if selected_course_id and selected_course_id != 'all':
        exams = Exam.objects.filter(course11_id=selected_course_id)
    else:
        exams = Exam.objects.all()

    # Implement pagination: Show 10 exams per page
    paginator = Paginator(exams, 10)  # 10 exams per page
    page_number = request.GET.get('page')
    exams_page = paginator.get_page(page_number)

    # Pass courses, filtered exams, and pagination details to the template
    context = {
        'exams': exams_page,
        'courses': courses,
        'selected_course_id': selected_course_id,  # To preserve filter state
    }
    return render(request, 'exams/view_exams.html', context)
