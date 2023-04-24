from django.shortcuts import render, redirect
from core.models import Equipo
from core.forms import EquipoForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# LOGIN

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from perfil.models import Avatar

from django.core.cache import cache

# Create your views here.

@login_required(redirect_field_name='next')
def inicio(request):
    total = cache.get("contador", 0)
    total += 1
    cache.set("contador", total)
    try:
        avatar = Avatar.objects.get(user=request.user)
        context = {'imagen': avatar.imagen.url}
    except Avatar.DoesNotExist:
        context = {}

    return render(request, 'core/index.html', context)

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
