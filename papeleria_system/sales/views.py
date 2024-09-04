from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from .models import Venta, DetalleVenta
from customers.models import Cliente
from products.models import Producto
import json
from django.core.serializers.json import DjangoJSONEncoder

def registrar_venta(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    mensaje_error = None
    cliente = None
    detalles = []

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

    if request.method == 'POST' and 'registrar_venta' in request.POST:
        cliente_id = request.POST.get('cliente_id')
        if not cliente_id:
            mensaje_error = "Debe ingresar un cliente válido."
        else:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                mensaje_error = "Debe ingresar un cliente válido."

        productos_seleccionados = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        if not productos_seleccionados or not cantidades or not cliente:
            mensaje_error = "Debe seleccionar al menos un producto y una cantidad válida."
        
        if not mensaje_error:
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
                        DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad, precio=producto.precio)
                        producto.stock -= cantidad
                        producto.save()
                        total_venta += total
                else:
                    venta.total = total_venta
                    venta.save()

                    # Devolver el venta_id en la respuesta JSON
                    return JsonResponse({'success': True, 'venta_id': venta.id})

    context = {
        'clientes': clientes,
        'productos': productos,
        'mensaje_error': mensaje_error,
        'detalles': detalles,
        'cliente': cliente,
    }
    return render(request, 'sales/registrar_venta.html', context)


def ver_factura(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)

    # Crear una lista de detalles con el cálculo del total por producto
    detalles_list = []
    for detalle in detalles:
        detalles_list.append({
            'producto__nombre': detalle.producto.nombre,
            'cantidad': detalle.cantidad,
            'precio': detalle.precio,
            'total': detalle.cantidad * detalle.precio  # Calcula el total
        })

    detalles_json = json.dumps(detalles_list, cls=DjangoJSONEncoder)

    context = {
        'venta': venta,
        'detalles': detalles,
        'detalles_json': detalles_json,  # Añadir detalles como JSON
    }

    return render(request, 'sales/factura.html', context)
