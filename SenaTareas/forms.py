from django import forms
from .models import User

class LoginForm(forms.Form):
    cc = forms.CharField(label='Cédula de Ciudadanía', max_length=20)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['cc', 'password', 'nombre', 'apellido', 'telefono', 'rol']