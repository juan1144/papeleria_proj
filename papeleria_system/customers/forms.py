from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'correo', 'direccion', 'fecha_nacimiento', 'identificacion_personal']

    # Validar el teléfono para que tenga al menos 9 dígitos
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and len(telefono) < 9:
            raise ValidationError("El número de teléfono debe tener al menos 9 caracteres.")
        return telefono

    # Validar el correo electrónico para que tenga la estructura correcta
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo and "@" not in correo:
            raise ValidationError("Ingrese un correo electrónico válido.")
        return correo

    # Validar que la identificación personal tenga solo números y tenga 9 dígitos
    def clean_identificacion_personal(self):
        identificacion_personal = self.cleaned_data.get('identificacion_personal')
        if not identificacion_personal.isdigit():
            raise ValidationError("La identificación personal debe contener solo números.")
        if len(identificacion_personal) != 9:
            raise ValidationError("La identificación personal debe tener exactamente 9 dígitos.")
        return identificacion_personal
