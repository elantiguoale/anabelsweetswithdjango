from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def register_view(request):
    """
    View for user registration
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register_simple.html', {'form': form})


def login_view(request):
    """
    View for user login
    """
    # Clear any existing messages to prevent queuing
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login_simple.html', {'form': form})


@login_required
def logout_view(request):
    """
    View for user logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """
    View for user profile (protected route example)
    """
    return render(request, 'accounts/profile_simple.html')


def test_view(request):
    """
    Test view to verify template loading
    """
    return render(request, 'accounts/test.html')
