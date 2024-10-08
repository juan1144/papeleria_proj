from django.shortcuts import render, redirect, get_object_or_404
from products.models import Producto
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.formats import number_format

def agregar_productos(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        umbral_stock = request.POST.get('umbral_stock')

        # Validaciones
        if Producto.objects.filter(codigo=codigo).exists():
            messages.error(request, "El código ingresado ya existe.")
        elif float(precio_compra) <= 0:
            messages.error(request, "El precio de compra debe ser mayor a 0.")
        elif float(precio) <= float(precio_compra):
            messages.error(request, "El precio de venta debe ser mayor que el precio de compra.")
        elif int(stock) <= 0:
            messages.error(request, "El stock no puede ser menor a 0.")
        elif int(umbral_stock) <= 0:
            messages.error(request, "El umbral de stock debe ser mayor a 0.")
        else:
            # Si pasa todas las validaciones, guardar el producto
            producto = Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                precio_compra=precio_compra,
                precio=precio,
                stock=stock,
                umbral_stock=umbral_stock,
            )
            messages.success(request, "Producto agregado exitosamente.")
            return redirect('ver_productos')

    categorias = ['Útiles Escolares', 'Tecnología', 'Oficina', 'Arte y Manualidades', 'Papelería General']
    
    context = {
        'categorias': categorias
    }
    return render(request, 'products/agregar_productos.html', context)

def ver_productos(request):
    # Obtener todos los productos
    productos = Producto.objects.all()

    # Filtros
    codigo = request.GET.get('codigo')
    nombre = request.GET.get('nombre')
    categoria = request.GET.get('categoria')
    orden = request.GET.get('orden')

    # Aplicar los filtros si se proporcionan
    if codigo:
        productos = productos.filter(codigo__icontains=codigo)
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)

    # Aplicar el orden si se proporciona
    if orden == 'precio_mayor':
        productos = productos.order_by('-precio')
    elif orden == 'precio_menor':
        productos = productos.order_by('precio')
    elif orden == 'stock_mayor':
        productos = productos.order_by('-stock')
    elif orden == 'stock_menor':
        productos = productos.order_by('stock')

    # Paginación - Mostrar 10 productos por página
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    productos_page_obj = paginator.get_page(page_number)

    context = {
        'productos': productos_page_obj,
        'codigo': codigo,
        'nombre': nombre,
        'categoria': categoria,
        'orden': orden,
    }

    return render(request, 'products/ver_productos.html', context)

def editar_producto(request, producto_id):
    # Obtener el producto por ID o devolver un error 404 si no existe
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        umbral_stock = request.POST.get('umbral_stock')

        # Validaciones
        if Producto.objects.filter(codigo=codigo).exclude(id=producto.id).exists():
            messages.error(request, "El código ingresado ya existe para otro producto.")
        elif float(precio_compra) <= 0:
            messages.error(request, "El precio de compra debe ser mayor a 0.")
        elif float(precio) <= float(precio_compra):
            messages.error(request, "El precio de venta debe ser mayor que el precio de compra.")
        elif int(stock) <= 0:
            messages.error(request, "El stock no puede ser negativo.")
        elif int(umbral_stock) <= 0:
            messages.error(request, "El umbral de stock no puede ser negativo.")
        else:
            # Si pasa todas las validaciones, actualizamos el producto
            producto.codigo = codigo
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.categoria = categoria
            producto.precio_compra = precio_compra
            producto.precio = precio
            producto.stock = stock
            producto.umbral_stock = umbral_stock
            producto.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('ver_productos')

    # Convertir el precio_compra y precio a formato con punto decimal para los inputs de tipo number
    producto.precio_compra = f"{producto.precio_compra:.2f}".replace(',', '.')
    producto.precio = f"{producto.precio:.2f}".replace(',', '.')

    context = {
        'producto': producto
    }
    return render(request, 'products/editar_producto.html', context)


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('ver_productos')