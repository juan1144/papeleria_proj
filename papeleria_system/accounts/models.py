from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('empleado', 'Empleado'),
    )
    identificacion_personal = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='empleado')

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rol})'
