from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def index(request):
    records = Record.objects.all()
    # check if user is logged in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('index')
        else:
            messages.error(request, "There was an error logging in, please try again.")
            return redirect('index')
    return render(request, 'index.html', {'records': records})

def login_user(request):
    # Optional: use this if you want a separate login page
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out of your account.")
    return redirect('index')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['password1']
            user = authenticate(username=username, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully created an account.")
                return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})
