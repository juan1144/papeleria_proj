from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

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

