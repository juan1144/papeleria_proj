from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    path('factura/<int:venta_id>/', views.ver_factura, name='ver_factura'),
]

