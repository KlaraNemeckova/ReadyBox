from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Package
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, "home.html") 

def about(request):
    return render(request, "about.html") 

def privacy_policy(request):
    return render(request, "privacy_policy.html") 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm()  # Vytvoření prázdného formuláře

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Získání dat z formuláře
        if form.is_valid():  # Pokud jsou data platná
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Přihlášení uživatele
                return redirect('user_dashboard' if not user.is_staff else 'admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})  # Vrácení formuláře do šablony



def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_dashboard(request):
    packages = Package.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'packages': packages})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='login')  # Pokud uživatel není admin, bude přesměrován na přihlašovací stránku.
def admin_dashboard(request):
    packages = Package.objects.all()
    return render(request, 'admin_dashboard.html', {'packages': packages})


