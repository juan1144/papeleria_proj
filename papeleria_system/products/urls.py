from django.urls import path
from . import views

urlpatterns = [
    path('ver/', views.ver_productos, name='ver_productos'),
    path('agregar/', views.agregar_productos, name='agregar_productos'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
