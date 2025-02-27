
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages

User = get_user_model()

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("userpassword")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")  # Redirect to index after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

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
