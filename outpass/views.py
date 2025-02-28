
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Student, Outpass,User,UserProfile,Parent,Faculty
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
import datetime
User = get_user_model()

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def login_view(request):
    message = None  
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("userpassword")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)  # Get the user's profile
            
            if user_profile.role == "Student":
                return redirect("index")  
            elif user_profile.role == "Faculty":
                return redirect("faculty")  # Redirect faculty to faculty dashboard
            elif user_profile.role == "Parent":
                return redirect("index")  # Redirect parents to index (or parent-specific page)

        else:
            message = "Invalid username or password"

    return render(request, 'login.html', {"message": message})

def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["useremail"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        role = request.POST["role"]

        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, "signin.html")

        # Create user and user profile
        new_user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfile.objects.create(user=new_user, role=role)

        # Handle role-specific data
        if role == "Student":
            roll_number = request.POST.get("roll_number", "")
            department = request.POST.get("department", "")
            year_of_study = request.POST.get("year_of_study", "1")  # Default to 1st year
            Student.objects.create(user_profile=user_profile, roll_number=roll_number, department=department, year_of_study=year_of_study)

        elif role == "Faculty":
            employee_id = request.POST.get("employee_id", "")
            department = request.POST.get("department", "")
            subject = request.POST.get("subject", "")
            Faculty.objects.create(user_profile=user_profile, employee_id=employee_id, department=department, subject=subject)

        elif role == "Parent":
            child_id = request.POST.get("child_id", "")
            relation = request.POST.get("relation", "")
            parent_name = username  # Using username as parent name
            student = Student.objects.filter(roll_number=child_id).first()
            if student:
                Parent.objects.create(user_profile=user_profile, student=student, parent_name=parent_name, relation_to_student=relation)
            else:
                messages.error(request, "Invalid student roll number for parent account.")
                return render(request, "signin.html")

        login(request, new_user)  # Log in the user after signup
        messages.success(request, f"Welcome, {username}! Your account has been created.")
        return redirect("index")  # Redirect to index after signup

    return render(request, "signin.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def apply_view(request):
    try:
        student = Student.objects.get(user_profile__user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "You are not registered as a student.")
        return redirect('index') 
    
    if request.method == "POST":
        # Get data from the HTML form
        reason = request.POST.get('reason')
        destination = request.POST.get('destination')
        departure_time = request.POST.get('from_date')
        return_time = request.POST.get('to_date')

        if not (reason and destination and departure_time and return_time):
            messages.error(request, "All fields are required.")
            return redirect('apply')  # Reload form if validation fails
        
        # Convert date strings to DateTime format
        departure_time = make_aware(datetime.datetime.strptime(departure_time, "%Y-%m-%d"))
        return_time = make_aware(datetime.datetime.strptime(return_time, "%Y-%m-%d"))

        # Save to database
        outpass = Outpass.objects.create(
            student=student,
            reason=reason,
            destination=destination,
            departure_time=departure_time,
            return_time=return_time
        )
        outpass.save()
        messages.success(request, "Outpass application submitted successfully.")
        return redirect('index')  # Redirect to a dashboard or confirmation page

    return render(request, 'apply.html', {'student': student})

@login_required
def faculty_dashboard(request):
    pending_outpasses = Outpass.objects.filter(status='Pending')  # Fetch pending outpasses
    return render(request, "Faculty.html", {"pending_outpasses": pending_outpasses})

@login_required
def approve_outpass(request, outpass_id):
    if request.method == "POST":
        try:
            outpass = Outpass.objects.get(id=outpass_id)
            outpass.status = "Approved"
            outpass.save()
            messages.success(request, "Outpass approved successfully.")
        except Outpass.DoesNotExist:
            messages.error(request, "Outpass not found.")
    return redirect("faculty")


@login_required
def reject_outpass(request, outpass_id):
    if request.method == "POST":
        try:
            outpass = Outpass.objects.get(id=outpass_id)
            outpass.status = "Rejected"
            outpass.save()
            messages.success(request, "Outpass rejected successfully.")
        except Outpass.DoesNotExist:
            messages.error(request, "Outpass not found.")
    return redirect("faculty")

