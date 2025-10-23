from django import forms
from django.core.exceptions import ValidationError
from .models import Persona
from datetime import date

class PersonaForm(forms.ModelForm):
    """
    Formulario personalizado para crear/editar Personas
    """
    
    class Meta:
        model = Persona
        fields = [
            'Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno',
            'Sexo', 'Fecha_nacimiento', 'Telefono', 'Direccion', 'Email'
        ]
        widgets = {
            'Rut': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '12345678-9',
                'maxlength': '12',
                'required': True
            }),
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Juan',
                'required': True
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'García',
                'required': True
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'López',
                'required': True
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
                'required': True
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '+56912345678'
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Calle, número, comuna'
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'correo@ejemplo.com'
            }),
        }
        labels = {
            'Rut': 'RUT',
            'Nombre': 'Nombre',
            'Apellido_Paterno': 'Apellido Paterno',
            'Apellido_Materno': 'Apellido Materno',
            'Sexo': 'Sexo',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Email': 'Correo Electrónico'
        }

    def clean_Rut(self):
        """Validar que el RUT sea único"""
        rut = self.cleaned_data.get('Rut')
        if rut:
            # Si es edición, excluir el registro actual
            if self.instance.pk:
                if Persona.objects.exclude(pk=self.instance.pk).filter(Rut=rut).exists():
                    raise ValidationError('Este RUT ya está registrado en el sistema.')
            else:
                if Persona.objects.filter(Rut=rut).exists():
                    raise ValidationError('Este RUT ya está registrado en el sistema.')
        return rut

    def clean_Fecha_nacimiento(self):
        """Validar fecha de nacimiento"""
        fecha = self.cleaned_data.get('Fecha_nacimiento')
        if fecha:
            hoy = date.today()
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            
            if edad < 0:
                raise ValidationError('La fecha de nacimiento no puede ser futura.')
            if edad > 120:
                raise ValidationError('La fecha de nacimiento no es válida.')
        return fecha