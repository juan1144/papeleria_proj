from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    context = {
        'username': request.user.username,
        'full_name': f"{request.user.nombre} {request.user.apellido}"  # Asegúrate que estos campos existan en el modelo User
    }
    return render(request, 'home.html', context)
