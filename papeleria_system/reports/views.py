from django.shortcuts import render
from sales.models import Venta, DetalleVenta
from django.db.models import Sum, F, FloatField
import datetime
import json
from django.contrib import messages

def reportes_ventas_categoria(request):
    # Obtener las fechas del filtro
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    # Establecer fechas por defecto si no se proporcionan
    if not fecha_desde:
        fecha_desde = datetime.date.today().replace(day=1)  # Primer día del mes actual
    else:
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()

    if not fecha_hasta:
        fecha_hasta = datetime.date.today()  # Fecha actual
    else:
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()

    # Convertir las fechas a datetime para que el filtro funcione correctamente
    fecha_desde_dt = datetime.datetime.combine(fecha_desde, datetime.time.min)
    fecha_hasta_dt = datetime.datetime.combine(fecha_hasta, datetime.time.max)

    # Filtrar las ventas según las fechas y calcular las ganancias
    ventas = DetalleVenta.objects.filter(
        venta__creado_en__range=[fecha_desde_dt, fecha_hasta_dt]
    ).values(
        'producto__categoria'
    ).annotate(
        cantidad_vendida=Sum('cantidad'),
        ganancias=Sum((F('precio') - F('producto__precio_compra')) * F('cantidad'), output_field=FloatField())
    ).order_by('producto__categoria')

    # Preparar datos para el gráfico de pastel
    categorias = [venta['producto__categoria'] for venta in ventas]
    cantidades = [venta['cantidad_vendida'] for venta in ventas]

    # Asegurarse de que las fechas se formateen en 'yyyy-MM-dd'
    context = {
        'ventas': ventas,
        'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),
        'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d'),
        'categorias': json.dumps(categorias),
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
    else:
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()

    if not fecha_hasta:
        fecha_hasta = datetime.date.today()  # Fecha actual
    else:
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()

    # Convertir las fechas a datetime para que el filtro funcione correctamente
    fecha_desde_dt = datetime.datetime.combine(fecha_desde, datetime.time.min)
    fecha_hasta_dt = datetime.datetime.combine(fecha_hasta, datetime.time.max)

    # Filtrar las ventas según las fechas
    ventas = DetalleVenta.objects.filter(
        venta__creado_en__range=[fecha_desde_dt, fecha_hasta_dt]
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

    # Asegurarse de que las fechas se formateen en 'yyyy-MM-dd'
    context = {
        'ventas': ventas,
        'fecha_desde': fecha_desde.strftime('%Y-%m-%d'),
        'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d'),
        'productos': json.dumps(productos),
        'cantidades': json.dumps(cantidades),
    }

    return render(request, 'reports/reportes_productos_mas_vendidos.html', context)
