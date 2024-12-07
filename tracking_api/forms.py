from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Package

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['tracking_number', 'status', 'pickup_code', 'user']
        widgets = {
            'status': forms.Select(choices=Package.STATUS_CHOICES),  # Udržuje vlastní výběr pro status
        }

    # Vytvoří pole pro výběr uživatele
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

