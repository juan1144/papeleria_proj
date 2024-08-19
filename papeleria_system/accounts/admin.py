from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 
        'email', 
        'nombre', 
        'apellido', 
        'identificacion_personal', 
        'telefono', 
        'rol', 
        'is_active', 
        'is_staff'
    )
    search_fields = (
        'username', 
        'email', 
        'nombre', 
        'apellido', 
        'identificacion_personal', 
        'telefono', 
        'rol'
    )
    ordering = ('username',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'nombre', 
                'apellido', 
                'identificacion_personal', 
                'telefono', 
                'rol', 
                'password1', 
                'password2', 
                'is_active', 
                'is_staff'
            ),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': (
                'nombre', 
                'apellido', 
                'email', 
                'identificacion_personal', 
                'telefono', 
                'rol'
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            )
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

admin.site.register(User, UserAdmin)
