from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm



def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("dashboard")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/signup.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
       
        
        # Validate inputs
        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, "registration/login.html")
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "registration/login.html")  # IMPORTANT: return here
        elif not user.is_active:
            messages.error(request, "Please verify your email.")
            return render(request, "registration/login.html")  # IMPORTANT: return here
        else:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect("dashboard")

    return render(request, "registration/login.html")

def logout_view(request):
    """
    Handle user logout
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    
    # If GET request, redirect to dashboard
    return redirect('dashboard')