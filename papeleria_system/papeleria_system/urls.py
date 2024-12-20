"""
URL configuration for papeleria_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view
from .views import home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),
    
    path('login/', login_view, name='login'),
    path('', login_view),

    # Incluyendo las URLs de cada aplicación

    path('home/', home_view, name='home'),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
    path('clientes/', include('customers.urls')),

    # Ruta para cerrar sesión, usando la vista estándar de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
