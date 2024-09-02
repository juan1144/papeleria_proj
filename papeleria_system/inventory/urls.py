from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_inventory, name='view_inventory'),
    path('add/', views.add_inventory, name='add_inventory'),
    path('alerta/', views.alerta_stock, name='alerta_stock'),
]
