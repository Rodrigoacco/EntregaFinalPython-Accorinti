from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EquipoForm(forms.Form):
    name = forms.CharField(max_length=20)
    n_camada = forms.IntegerField()

class UserRegisterForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        help_texts = {k:"" for k in fields}