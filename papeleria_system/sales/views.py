from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from .models import Venta, DetalleVenta
from customers.models import Cliente
from products.models import Producto
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator

# Vista para registrar una nueva venta
def registrar_venta(request):
    # Obtener todos los clientes y productos disponibles
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    mensaje_error = None
    cliente = None
    detalles = []

    # Manejar la búsqueda de un cliente por su número de DUI
    if request.method == 'POST' and 'buscar_cliente' in request.POST:
        dui = request.POST.get('dui')
        try:
            cliente = Cliente.objects.get(identificacion_personal=dui)
            return JsonResponse({
                'id': cliente.id,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'correo': cliente.correo,
                'telefono': cliente.telefono,
            })
        except Cliente.DoesNotExist:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    # Manejar la acción de registrar una venta
    if request.method == 'POST' and 'registrar_venta' in request.POST:
        cliente_id = request.POST.get('cliente_id')
        if not cliente_id:
            mensaje_error = "Debe ingresar un cliente válido."
        else:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                mensaje_error = "Debe ingresar un cliente válido."

        # Obtener productos y cantidades seleccionados
        productos_seleccionados = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        if not productos_seleccionados or not cantidades or not cliente:
            mensaje_error = "Debe seleccionar al menos un producto y una cantidad válida."
        
        if not mensaje_error:
            # Registrar la venta de forma atómica
            with transaction.atomic():
                venta = Venta.objects.create(cliente=cliente, usuario=request.user, total=0)
                total_venta = 0
                for i in range(len(productos_seleccionados)):
                    producto = Producto.objects.get(id=productos_seleccionados[i])
                    cantidad = int(cantidades[i])
                    if cantidad > producto.stock:
                        mensaje_error = f"No hay suficiente stock para {producto.nombre}."
                        break
                    else:
                        total = cantidad * producto.precio
                        DetalleVenta.objects.create(
                            venta=venta, 
                            producto=producto, 
                            cantidad=cantidad, 
                            precio=producto.precio
                        )
                        producto.stock -= cantidad
                        producto.save()
                        total_venta += total
                else:
                    # Guardar el total de la venta
                    venta.total = total_venta
                    venta.save()

                    # Retornar el ID de la venta como respuesta JSON
                    return JsonResponse({'success': True, 'venta_id': venta.id})

    context = {
        'clientes': clientes,
        'productos': productos,
        'mensaje_error': mensaje_error,
        'detalles': detalles,
        'cliente': cliente,
    }
    return render(request, 'sales/registrar_venta.html', context)

# Vista para mostrar la factura de una venta
def ver_factura(request, venta_id):
    # Obtener la venta por su ID o retornar un 404 si no existe
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    # Crear una lista de detalles de productos para mostrar en la factura
    detalles_list = []
    for detalle in detalles:
        detalles_list.append({
            'producto__nombre': detalle.producto.nombre,
            'cantidad': detalle.cantidad,
            'precio': detalle.precio,
            'total': detalle.cantidad * detalle.precio  # Calcular el total del producto
        })

    detalles_json = json.dumps(detalles_list, cls=DjangoJSONEncoder)

    context = {
        'venta': venta,
        'detalles': detalles,
        'detalles_json': detalles_json,
    }

    return render(request, 'sales/factura.html', context)

# Vista para listar todas las ventas
def listar_ventas(request):
    # Obtener todas las ventas y detalles de ventas
    ventas = Venta.objects.all()
    detalles_ventas = DetalleVenta.objects.all()

    # Aplicar filtros según la solicitud
    factura_id = request.GET.get('factura_id')
    cliente_dui = request.GET.get('cliente_dui')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    producto = request.GET.get('producto')

    if factura_id:
        ventas = ventas.filter(id=factura_id)
    if cliente_dui:
        ventas = ventas.filter(cliente__identificacion_personal__icontains=cliente_dui)
    if fecha_desde and fecha_hasta:
        ventas = ventas.filter(creado_en__date__range=[fecha_desde, fecha_hasta])
    if producto:
        detalles_ventas = detalles_ventas.filter(producto__nombre__icontains=producto)

    # Paginación - Mostrar 8 detalles de ventas por página
    paginator = Paginator(detalles_ventas, 8)
    page_number = request.GET.get('page')
    detalles_page_obj = paginator.get_page(page_number)

    context = {
        'ventas': ventas,
        'detalles_ventas': detalles_page_obj,
        'factura_id': factura_id,
        'cliente_dui': cliente_dui,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'producto': producto,
    }

    return render(request, 'sales/listar_ventas.html', context)
