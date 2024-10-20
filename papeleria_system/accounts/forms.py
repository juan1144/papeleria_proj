from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'identificacion_personal', 'nombre', 'apellido', 'telefono', 'rol', 'password1', 'password2']

# forms.py
class UserForm(forms.ModelForm):
    nueva_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label='Nueva Contraseña',
        help_text='Dejar vacío para no cambiar la contraseña.'
    )

    class Meta:
        model = User
        fields = ['username', 'identificacion_personal', 'nombre', 'apellido', 'telefono', 'rol', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'identificacion_personal': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
