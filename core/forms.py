from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'span2','placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'span2','placeholder':'Contraseña'}))