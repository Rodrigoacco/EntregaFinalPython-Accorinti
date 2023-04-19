from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import inicio, notFound, agregar, mostrar, editar, eliminar, empleados, login_request, register

urlpatterns = [
    path('', inicio, name="index"),
    path('/', notFound, name="notFound"),
    path('empleados/', empleados, name="empleados"),
    path('agregar/', agregar, name="agregar"),
    path('mostrar/', mostrar, name="mostrar"),
    path('editar/<int:id_equipo>/', editar, name="editar"),
    path('eliminar/<int:id_equipo>/', eliminar, name="eliminar"),
]

urlpatterns += [
    path('login/', login_request, name="login"),
    path('register/', register, name="registro"),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name="Logout"),
]