from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Package
from .forms import RegistrationForm, PackageForm
from django.contrib import messages
from django.views.generic import ListView


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
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('user_dashboard' if not user.is_staff else 'admin_dashboard')
        else:
            messages.error(request, "Invalid username or password.") 

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='login')  # Pokud uživatel není admin, bude přesměrován na přihlašovací stránku.
def admin_dashboard(request):
    packages = Package.objects.all()
    return render(request, 'admin_dashboard.html', {'packages': packages})



@login_required
def user_dashboard(request):
    if request.method == "POST":
        tracking_number = request.POST.get("tracking_number", "").strip()

        # Pokud uživatel nezadal tracking_number
        if not tracking_number:
            messages.error(request, "Please enter a tracking number.")
            return redirect('user_dashboard')

        try:
            # Najděte balík podle tracking_number
            package = Package.objects.get(tracking_number=tracking_number)
            # Přesměrujte uživatele na stránku package_status
            return redirect('package_status', tracking_number=package.tracking_number)
        except Package.DoesNotExist:
            # Pokud balík neexistuje, zobrazte zprávu na user_dashboard
            messages.error(request, "Package not found. Please check the tracking number.")
            return redirect('user_dashboard')

    # GET request: zobrazí dashboard
    return render(request, 'user_dashboard.html')


@login_required
def package_status(request, tracking_number):
    try:
        package = Package.objects.get(tracking_number=tracking_number, user=request.user)
        print(f"Package found: {package.tracking_number}, {package.status}")
    except Package.DoesNotExist:
        messages.error(request, "Package not found.")
        return redirect('user_dashboard')
    
    return render(request, 'package_status.html', {'package': package})



@login_required
def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            # Přidání uživatele, který zásilku vytvořil
            package = form.save(commit=False)
            package.user = request.user
            package.save()
            return redirect('admin_dashboard')  # Přesměrování na seznam zásilek
    else:
        form = PackageForm()

    return render(request, 'add_package.html', {'form': form})


class PackageListView(ListView):
    model = Package
    template_name = 'packages_list.html'
    context_object_name = 'packages'

    def get_queryset(self):
        # Filtrace zásilek pro aktuálního uživatele
        return Package.objects.filter(user=self.request.user)


def package_history(request, tracking_number):
    package = get_object_or_404(Package, tracking_number=tracking_number)
    history = package.history.all()  

    return render(request, 'package_history.html', {'package': package, 'history': history})



