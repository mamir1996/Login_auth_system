from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .forms import SignupForm, SigninForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.create_user(
                username=cleaned_data['user_name'],
                first_name=cleaned_data['first_name'],
                last_name=cleaned_data['last_name'],
                email=cleaned_data['email'],
                # phone_num=cleaned_data['phone_num'],
                password=cleaned_data['password']
            )
            user.save()
            messages.success(request, "Your account has been successfully created.")
            return redirect('signin')
        else:
            messages.error(request, "Please correct the errors below.")
            
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            messages.success(request, f"Welcome back {form.cleaned_data['username']}!")
            return redirect('home')  # or wherever you want
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = SigninForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')
