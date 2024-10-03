from django.shortcuts import render, redirect, get_object_or_404
from customers.models import Cliente
from django.contrib import messages
import re
from django.core.paginator import Paginator
from datetime import datetime, timedelta

def calcular_edad(fecha_nacimiento):
    hoy = datetime.today().date()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        identificacion_personal = request.POST.get('identificacion_personal')

        # Validaciones
        if len(telefono) != 8 or not telefono.isdigit():
            messages.error(request, "El número de teléfono debe contener exactamente 8 dígitos y solo números.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            messages.error(request, "Por favor, ingrese un correo electrónico válido.")
        elif not re.match(r"^\d{9}$", identificacion_personal):
            messages.error(request, "La identificación personal debe tener exactamente 9 dígitos numéricos.")
        elif not fecha_nacimiento:
            messages.error(request, "La fecha de nacimiento no puede estar vacía.")
        else:
            fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            if calcular_edad(fecha_nacimiento_obj) < 18:
                messages.error(request, "El cliente debe tener al menos 18 años.")
            # Verificar si el DUI ya existe en la base de datos
            elif Cliente.objects.filter(identificacion_personal=identificacion_personal).exists():
                messages.error(request, "Ya existe un cliente con este DUI.")
            else:
                # Si pasa todas las validaciones, guardar el cliente
                cliente = Cliente.objects.create(
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    correo=correo,
                    direccion=direccion,
                    fecha_nacimiento=fecha_nacimiento,
                    identificacion_personal=identificacion_personal,
                )
                messages.success(request, "Cliente agregado exitosamente.")
                return redirect('ver_clientes')
    
    return render(request, 'customers/agregar_cliente.html')

def ver_clientes(request):
    # Obtener todos los clientes
    clientes = Cliente.objects.all()

    # Filtros
    dui = request.GET.get('dui')
    nombre = request.GET.get('nombre')
    apellido = request.GET.get('apellido')
    telefono = request.GET.get('telefono')
    correo = request.GET.get('correo')

    # Aplicar los filtros si se proporcionan
    if dui:
        clientes = clientes.filter(identificacion_personal__icontains=dui)
    if nombre:
        clientes = clientes.filter(nombre__icontains=nombre)
    if apellido:
        clientes = clientes.filter(apellido__icontains=apellido)
    if telefono:
        clientes = clientes.filter(telefono__icontains=telefono)
    if correo:
        clientes = clientes.filter(correo__icontains=correo)

    # Paginación - Mostrar 10 clientes por página
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clientes_page_obj = paginator.get_page(page_number)

    context = {
        'clientes': clientes_page_obj,
        'dui': dui,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'correo': correo,
    }

    return render(request, 'customers/ver_clientes.html', context)

# Vista para eliminar cliente
def eliminar_cliente(request, client_id):
    cliente = get_object_or_404(Cliente, id=client_id)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('ver_clientes')

# Vista para editar cliente
def editar_cliente(request, client_id):
    cliente = get_object_or_404(Cliente, id=client_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        identificacion_personal = request.POST.get('identificacion_personal')

        if len(telefono) != 8 or not telefono.isdigit():
            messages.error(request, "El número de teléfono debe contener exactamente 8 dígitos y solo números.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            messages.error(request, "Por favor, ingrese un correo electrónico válido.")
        elif not re.match(r"^\d{9}$", identificacion_personal):
            messages.error(request, "La identificación personal debe tener exactamente 9 dígitos numéricos.")
        elif not fecha_nacimiento:
            messages.error(request, "La fecha de nacimiento no puede estar vacía.")
        else:
            fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            if calcular_edad(fecha_nacimiento_obj) < 18:
                messages.error(request, "El cliente debe tener al menos 18 años.")
            # Verificar si el DUI ya existe en la base de datos, pero ignorar el cliente actual
            elif Cliente.objects.filter(identificacion_personal=identificacion_personal).exclude(id=client_id).exists():
                messages.error(request, "Ya existe otro cliente con este DUI.")
            else:
                cliente.nombre = nombre
                cliente.apellido = apellido
                cliente.telefono = telefono
                cliente.correo = correo
                cliente.direccion = direccion
                cliente.fecha_nacimiento = fecha_nacimiento
                cliente.identificacion_personal = identificacion_personal
                cliente.save()
                messages.success(request, "Cliente actualizado correctamente.")
                return redirect('ver_clientes')

    context = {
        'cliente': cliente
    }
    return render(request, 'customers/editar_cliente.html', context)
