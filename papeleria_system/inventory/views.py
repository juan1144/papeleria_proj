from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Inventario
from products.models import Producto
from django.contrib import messages
from django.db.models import F

# Vista para ver el inventario
def view_inventory(request):
    # Obtener todos los inventarios y productos
    inventarios = Inventario.objects.all()
    productos = Producto.objects.all()

    # Obtener filtros desde la solicitud GET
    producto_id = request.GET.get('producto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    tipo_cambio = request.GET.get('tipo_cambio')

    # Aplicar filtro por producto
    if producto_id and producto_id != '':
        inventarios = inventarios.filter(producto_id=producto_id)

    # Aplicar filtro por rango de fechas
    if fecha_desde and fecha_hasta:
        inventarios = inventarios.filter(creado_en__range=[fecha_desde, fecha_hasta])

    # Aplicar filtro por tipo de transacción (entrada/salida)
    if tipo_cambio and tipo_cambio != '':
        inventarios = inventarios.filter(tipo_cambio=tipo_cambio)

    # Paginación: mostrar 10 registros por página
    paginator = Paginator(inventarios, 10)
    page_number = request.GET.get('page')
    inventarios = paginator.get_page(page_number)

    # Obtener nombre completo del usuario si está autenticado
    full_name = f"{request.user.nombre} {request.user.apellido}" if request.user.is_authenticated else ""

    context = {
        'inventarios': inventarios,
        'productos': productos,
        'producto_id': producto_id,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'tipo_cambio': tipo_cambio,
        'paginator': paginator,
        'full_name': full_name,
    }
    return render(request, 'inventory/view_inventory.html', context)

# Vista para agregar un nuevo movimiento de inventario (entrada/salida)
def add_inventory(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        # Obtener datos del formulario
        producto_id = request.POST.get('producto')
        cambio = request.POST.get('cambio')
        tipo_cambio = request.POST.get('tipo_cambio')
        motivo = request.POST.get('motivo')

        # Validar campos obligatorios
        if not producto_id or not cambio or not tipo_cambio:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'inventory/add_inventory.html', {'productos': productos, 'producto_id': producto_id, 'cambio': cambio, 'tipo_cambio': tipo_cambio, 'motivo': motivo})

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            messages.error(request, "El producto seleccionado no existe.")
            return redirect('add_inventory')

        cambio = int(cambio)

        # Validar y ajustar el stock según el tipo de transacción
        if tipo_cambio == 'entrada':
            producto.stock += cambio
            producto.save()
        elif tipo_cambio == 'salida':
            if producto.stock >= cambio:
                producto.stock -= cambio
                producto.save()
            else:
                messages.error(request, f"No hay suficiente stock para realizar la salida. Stock actual: {producto.stock}.")
                return render(request, 'inventory/add_inventory.html', {'productos': productos, 'producto_id': producto_id, 'cambio': cambio, 'tipo_cambio': tipo_cambio, 'motivo': motivo})

        # Crear registro en la tabla de inventarios
        Inventario.objects.create(
            producto=producto,
            cambio=cambio,
            tipo_cambio=tipo_cambio,
            motivo=motivo,
            usuario=request.user
        )

        messages.success(request, "Inventario actualizado correctamente.")
        return redirect('view_inventory')

    full_name = f"{request.user.nombre} {request.user.apellido}" if request.user.is_authenticated else ""
    
    context = {
        'productos': productos,
        'full_name': full_name,
    }
    return render(request, 'inventory/add_inventory.html', context)

# Vista para mostrar productos bajo stock mínimo
def alerta_stock(request):
    # Filtrar productos cuyo stock esté por debajo del umbral
    productos_bajo_stock = Producto.objects.filter(stock__lte=F('umbral_stock'))

    # Paginación: mostrar 10 productos por página
    paginator = Paginator(productos_bajo_stock, 10)
    page_number = request.GET.get('page')
    productos_bajo_stock = paginator.get_page(page_number)

    full_name = f"{request.user.nombre} {request.user.apellido}" if request.user.is_authenticated else ""

    context = {
        'productos_bajo_stock': productos_bajo_stock,
        'full_name': full_name,
    }
    return render(request, 'inventory/alerta_stock.html', context)
