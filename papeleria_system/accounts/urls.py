from django.urls import path
from . import views
from .views import CustomPasswordChangeView
from django.views.generic import TemplateView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('ver/', views.ver_usuarios, name='ver_usuarios'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('cambiar-password/', CustomPasswordChangeView.as_view(), name='cambiar_password'),
    path('cambiar-password/done/', TemplateView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]
