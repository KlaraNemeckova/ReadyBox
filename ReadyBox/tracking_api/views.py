from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Package
from .forms import RegistrationForm

def home(request):
    return render(request, "home.html") 

def about(request):
    return render(request, "about.html") 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('user_dashboard' if not user.is_staff else 'admin_dashboard')
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    packages = Package.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'packages': packages})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    packages = Package.objects.all()
    return render(request, 'admin_dashboard.html', {'packages': packages})


