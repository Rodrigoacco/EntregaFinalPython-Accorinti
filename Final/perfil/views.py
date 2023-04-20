from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from perfil.forms import UserRegisterForm, UserEditForm, AvatarForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from perfil.utilities.user_profile import clean_avatar_record_without_user

# Create your views here.

def login_request(request):
    msj = ""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contra)

            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return render(request, 'core/index.html')
            else:
                msj = "ERROR DE USUARIO"
        else:
            msj = "ERROR DE FORMULARIO"
    
    form = AuthenticationForm()
    return render(request, "perfil/login.html", {"form": form, "msj": msj})

def register(request):
    msj = "CREANDO USUARIO"
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            form.save()
            return render(request, "core/index.html", {"msj": f"Bienvenido {username}"})
        else:
            msj = "ERROR CREANDO USUARIO"
    
    form = UserRegisterForm()
    return render(request, "perfil/registro.html", {"form": form, "msj": msj})

@login_required
def perfil_edit(request):
    
    usuario = request.user

    if request.method == "POST":

        form = UserEditForm(request.POST)
        if form.is_valid():
            informacion = form.cleaned_data
            usuario.email = informacion["email"]
            usuario.password1 = informacion["password1"]
            usuario.password2 = informacion["password2"]
            usuario.save()

            return render(request, "core/index.html")

    else:
        data_dict = {
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
        }
        form = UserEditForm(initial=data_dict)
    return render(request, 'perfil/edit.html', {'form': form, 'usuario': usuario})

@login_required
def avatar_form(request):
    msj = "CARGANDO AVATAR"
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.save()
            avatar.user = request.user
            avatar.save()
            clean_avatar_record_without_user()
            return redirect(reverse('index'))
        else:
            msj = "ERROR CREANDO AVATAR, INVALIDO"
    
    form = AvatarForm()
    return render(request, "perfil/avatar_form.html", {"form": form, "msj": msj})
