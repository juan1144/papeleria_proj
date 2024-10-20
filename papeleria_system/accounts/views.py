from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, UserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash

def login_view(request):
    
    if request.method == 'POST':
        # Crear el formulario de autenticación con los datos enviados
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Extraer los datos validados del formulario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Autenticar al usuario con los datos proporcionados
            user = authenticate(username=username, password=password)

            if user is not None:
                # Si la autenticación es exitosa, iniciar sesión y redirigir a 'home'
                login(request, user)
                return redirect('home')

    else:
        # Si la solicitud es GET, renderizar un formulario vacío
        form = AuthenticationForm()
    
    # Renderizar la página de inicio de sesión con el formulario
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def agregar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('ver_usuarios')  # Redirigir a la lista de usuarios
        else:
            # Si el formulario no es válido, agrega mensajes de error específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/agregar_usuario.html', {'form': form})


@login_required
def ver_usuarios(request):
    # Obtener los parámetros de filtro del request
    identificacion_personal = request.GET.get('identificacion_personal')
    nombre = request.GET.get('nombre')
    apellido = request.GET.get('apellido')
    telefono = request.GET.get('telefono')
    rol = request.GET.get('rol')

    # Filtrar los usuarios basándose en los parámetros de búsqueda
    usuarios = User.objects.all()

    if identificacion_personal:
        usuarios = usuarios.filter(identificacion_personal__icontains=identificacion_personal)

    if nombre:
        usuarios = usuarios.filter(nombre__icontains=nombre)

    if apellido:
        usuarios = usuarios.filter(apellido__icontains=apellido)

    if telefono:
        usuarios = usuarios.filter(telefono__icontains=telefono)

    if rol:
        usuarios = usuarios.filter(rol=rol)

    # Paginación
    paginator = Paginator(usuarios, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    usuarios = paginator.get_page(page_number)

    context = {
        'usuarios': usuarios,
        'identificacion_personal': identificacion_personal,
        'nombre': nombre,
        'apellido': apellido,
        'telefono': telefono,
        'rol': rol,
    }
    
    return render(request, 'accounts/ver_usuarios.html', context)

# views.py
def editar_usuario(request, usuario_id):
    # Obtener el usuario por ID
    usuario = get_object_or_404(User, id=usuario_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)

            # Verificar si se ingresó una nueva contraseña
            nueva_password = form.cleaned_data.get('nueva_password')
            if nueva_password:
                usuario.set_password(nueva_password)

            usuario.save()
            messages.success(request, f'Usuario {usuario.username} actualizado correctamente.')
            return redirect('ver_usuarios')
    else:
        form = UserForm(instance=usuario)

    return render(request, 'accounts/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('ver_usuarios')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'accounts/cambiar_password.html'

    def form_valid(self, form):
        """Valida que la nueva contraseña no sea igual a la actual"""
        old_password = form.cleaned_data.get('old_password')
        new_password = form.cleaned_data.get('new_password1')

        # Verificar que la nueva contraseña no sea igual a la antigua
        if old_password == new_password:
            messages.error(self.request, 'La nueva contraseña no puede ser igual a la actual.')
            return self.form_invalid(form)

        # Si pasa la validación, actualizar la sesión y proceder
        user = form.save()
        update_session_auth_hash(self.request, user)  # Evitar que el usuario sea desconectado
        messages.success(self.request, 'Tu contraseña ha sido cambiada exitosamente.')
        return super().form_valid(form)
