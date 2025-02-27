
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
User = get_user_model()

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")
User = get_user_model()

def login_view(request):
    message = None  
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("userpassword")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")  
        else:
            message = "Invalid username or password"

    return render(request, 'login.html', {"message": message})


def sign_in(request):
    if request.method == "POST": 
        username = request.POST["username"]
        email = request.POST["useremail"]
        password = request.POST["password"]
        confirmpassword = request.POST["Confirmpassword"]  

        if password == confirmpassword:
            # Create user with hashed password
            new_user = User.objects.create_user(username=username, email=email, password=password)
            login(request, new_user)  # Log in the user after signup
            messages.success(request, f"Welcome, {username}! Your account has been created.")
            return redirect("index")  # Redirect to index after signup
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "signin.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
