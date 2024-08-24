from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Inventario
from products.models import Producto

def view_inventory(request):
    inventarios = Inventario.objects.all()
    productos = Producto.objects.all()

    # Filtros
    producto_id = request.GET.get('producto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    tipo_cambio = request.GET.get('tipo_cambio')

    if producto_id and producto_id != '':
        inventarios = inventarios.filter(producto_id=producto_id)

    if fecha_desde and fecha_hasta:
        inventarios = inventarios.filter(creado_en__range=[fecha_desde, fecha_hasta])

    if tipo_cambio and tipo_cambio != '':
        inventarios = inventarios.filter(tipo_cambio=tipo_cambio)

    # Paginación
    paginator = Paginator(inventarios, 10)  # Mostrar 10 registros por página
    page_number = request.GET.get('page')
    inventarios = paginator.get_page(page_number)

    # Usar nombre y apellido en lugar de first_name y last_name si esos son los campos en tu modelo de usuario
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


def add_inventory(request):
    # Lógica para agregar al inventario
    return render(request, 'inventory/add_inventory.html')
