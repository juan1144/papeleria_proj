from django.urls import path
from .views import agregar_cliente, ver_clientes, editar_cliente, eliminar_cliente

urlpatterns = [
    path('agregar/', agregar_cliente, name='agregar_cliente'),
    path('ver/', ver_clientes, name='ver_clientes'),
    path('editar/<int:client_id>/', editar_cliente, name='editar_cliente'),
    path('eliminar/<int:client_id>/', eliminar_cliente, name='eliminar_cliente'),
]
