from django.shortcuts import render
from core.models import Equipo
from core.forms import EquipoForm

# Create your views here.
def inicio (request):
    return render(request, 'core/index.html')

def empleados (request):
    return render(request, 'core/empleados.html')

def notFound (request):
    return render(request, 'core/notFound.html')

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
