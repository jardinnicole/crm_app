from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .forms import AddRecordForm
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

def customer_record(request, pk):
    if request.user.is_authenticated:
        # lookup
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('index')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "You have successfully deleted this record.")
        return redirect("index")
    else:
        messages.success(request, "You must be logged in to access this page.")

def add_record(request):
        form = AddRecordForm(request.POST or None)
        if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record added.")
                    return redirect('index')
            else:
                return render(request, 'add_record.html', {'form':form})
        else:
            messages.error(request, "You must be logged in to view this page.")
            return redirect('index')
        
def edit_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated.")
            return redirect('index')
        return render(request, 'edit_record.html', {'form': form, 'customer_record': current_record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('index')
