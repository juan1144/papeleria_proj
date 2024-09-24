from django.urls import path
from . import views

urlpatterns = [
    path('ventas_categoria/', views.reportes_ventas_categoria, name='reportes_ventas_categoria'),
    path('productos-mas-vendidos/', views.reportes_productos_mas_vendidos, name='reportes_productos_mas_vendidos'),
]
