from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from .models import todo 
def Signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")  # Assuming you added this to your form

        # Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, 'signup.html')

        try:
            # Create the user if all checks pass
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()  # This call is redundant but harmless.
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        except Exception as e:
            # Catch any other potential errors
            messages.error(request, f"An unexpected error occurred: {e}")
            return render(request, 'signup.html')

    else:
        # Handle GET request
        return render(request, 'signup.html')

def Login(request):
    """
    Handles user login.

    - Renders the login form on a GET request.
    - Authenticates user on a POST request.
    - Redirects to the dashboard on successful login.
    - Displays an error message on failed login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('todo')  # Redirect to the to-do list page
        else:
            # If authentication fails, display an error message
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html') # Re-render the form with the error
    
    else:
        # For a GET request, simply render the login page
        return render(request, 'login.html')
# In your views.py file

@login_required
def TodoList(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            models.todo.objects.create(title=title, user=request.user)
            messages.success(request, "To-do item added successfully!")
            return redirect('todo')
        else:
            messages.error(request, "To-do title cannot be empty.")
            return redirect('todo')
    
    todos = models.todo.objects.filter(user=request.user).order_by('-created_at')
    context = {'todos': todos} 
    return render(request, 'todo.html', context)


@login_required
def delete_todo(request, todo_id):
    if request.method == "POST":
        todo_item = get_object_or_404(todo, id=todo_id, user=request.user)
        todo_item.delete()
        messages.success(request, "To-do item deleted successfully!")
    return redirect('todo')


def Log(request):
    """
    Logs out the current user and redirects them to the home page or login page.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  