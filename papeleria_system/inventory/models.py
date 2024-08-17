from django.db import models
from django.conf import settings
from products.models import Producto

class Inventario(models.Model):
    TIPO_CAMBIO_CHOICES = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cambio = models.IntegerField()
    tipo_cambio = models.CharField(max_length=10, choices=TIPO_CAMBIO_CHOICES)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.tipo_cambio} - {self.cambio}"
