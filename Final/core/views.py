from django.shortcuts import render
from core.models import Equipo
from core.forms import EquipoForm, UserRegisterForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# LOGIN
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio (request):
    return render(request, 'core/index.html')

def empleados (request):
    return render(request, 'core/empleados.html')

def notFound (request):
    return render(request, 'core/notFound.html')

@login_required(redirect_field_name='next')
def mostrar (request):
    
    empleado = Equipo.objects.all()
    
    return render(request, 'core/mostrarEmpleado.html', {"empleados":empleado})

def agregar (request):
    
    if request.method == "POST":
        equipo_form = EquipoForm(request.POST)
        
        if equipo_form.is_valid():
            data = equipo_form.cleaned_data
            equipo = Equipo(nombre=data["name"], camada=data["n_camada"])
            equipo.save()
            return render(request, 'core/index.html')
    
    equipo_form = EquipoForm()
    return render(request, 'core/agregarEmpleado.html', {"form": equipo_form})

def eliminar (request, id_equipo):
    
    equipo = Equipo.objects.get(id=id_equipo)
    name = equipo.nombre
    equipo.delete()
    
    return render(request, 'core/eliminarEmpleado.html', {"nombre_eliminado": name})

def editar (request, id_equipo):
    
    equipo = Equipo.objects.get(id=id_equipo)
    
    if request.method == "POST":
        equipo_form = EquipoForm(request.POST)
        if equipo_form.is_valid():
            data = equipo_form.cleaned_data
            equipo.nombre = data["name"]
            equipo.camada = data["n_camada"]
            equipo.save()
            return render(request, 'core/index.html')
    else:
        equipo_form = EquipoForm(initial={'name': equipo.nombre, 'n_camada': equipo.camada})
    
    return render(request, 'core/editarEmpleado.html', {'form': equipo_form})

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
    return render(request, "core/login.html", {"form": form, "msj": msj})

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
    return render(request, "core/registro.html", {"form": form, "msj": msj})
