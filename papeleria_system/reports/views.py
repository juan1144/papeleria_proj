from django.shortcuts import render
from sales.models import Venta, DetalleVenta
from products.models import Producto
from django.db.models import Sum, F, FloatField
import datetime
import json

def reportes_ventas_categoria(request):
    # Obtener las fechas del filtro
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    # Establecer fechas por defecto si no se proporcionan
    if not fecha_desde:
        fecha_desde = datetime.date.today().replace(day=1)  # Primer día del mes actual
    if not fecha_hasta:
        fecha_hasta = datetime.date.today()  # Fecha actual

    # Filtrar las ventas según las fechas
    ventas = DetalleVenta.objects.filter(
        venta__creado_en__date__range=[fecha_desde, fecha_hasta]
    ).values(
        'producto__categoria'  # Cambiado para acceder al campo de texto de la categoría
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        ingreso=Sum(F('cantidad') * F('precio'), output_field=FloatField())
    ).order_by('producto__categoria')

    # Preparar datos para el gráfico de pastel
    categorias = [venta['producto__categoria'] for venta in ventas]
    cantidades = [venta['cantidad_vendida'] for venta in ventas]

    context = {
        'ventas': ventas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'categorias': json.dumps(categorias),  # Serializamos las listas para JavaScript
        'cantidades': json.dumps(cantidades),
    }

    return render(request, 'reports/reportes_ventas_categoria.html', context)

def reportes_productos_mas_vendidos(request):
    # Obtener las fechas del filtro
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    # Establecer fechas por defecto si no se proporcionan
    if not fecha_desde:
        fecha_desde = datetime.date.today().replace(day=1)  # Primer día del mes actual
    if not fecha_hasta:
        fecha_hasta = datetime.date.today()  # Fecha actual

    # Filtrar las ventas según las fechas
    ventas = DetalleVenta.objects.filter(
        venta__creado_en__date__range=[fecha_desde, fecha_hasta]
    ).values(
        'producto__nombre',
        'producto__precio_compra',
        'producto__precio'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        total_ganancias=Sum((F('precio') - F('producto__precio_compra')) * F('cantidad'), output_field=FloatField())
    ).order_by('-cantidad_vendida')[:6]  # Selecciona los 6 productos más vendidos

    # Preparar los datos para el gráfico de barras
    productos = [venta['producto__nombre'] for venta in ventas]
    cantidades = [venta['cantidad_vendida'] for venta in ventas]

    context = {
        'ventas': ventas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'productos': json.dumps(productos),  # Serializar las listas a JSON
        'cantidades': json.dumps(cantidades),  # Serializar las listas a JSON
    }

    return render(request, 'reports/reportes_productos_mas_vendidos.html', context)

