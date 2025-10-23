################
# FORMULARIO: Crear Persona
# Ubicación: apps/core/Forms/Form_crear_persona.py
################

from django import forms
from core.models import Persona
from utilities.validadores import validar_rut_chileno, validar_edad, validar_telefono


class Form_crear_persona(forms.ModelForm):
    """
    Formulario para crear una nueva persona.
    Usado por: Administrativo, Matrona, Médico
    """
    
    class Meta:
        model = Persona
        fields = ['rut', 'nombre', 'apellido', 'edad', 'direccion', 'contacto']
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12.345.678-9',
                'maxlength': '12'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'maxlength': '255'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido completo',
                'maxlength': '255'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad (12-60)',
                'min': '12',
                'max': '60',
                'type': 'number'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa',
                'rows': '3'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56912345678 o 912345678',
                'maxlength': '20'
            }),
        }
        labels = {
            'rut': 'RUT',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'edad': 'Edad',
            'direccion': 'Dirección',
            'contacto': 'Teléfono de Contacto',
        }
    
    def clean_rut(self):
        """Valida RUT chileno con dígito verificador"""
        rut = self.cleaned_data.get('rut')
        
        if not rut:
            raise forms.ValidationError('El RUT es obligatorio')
        
        # Validar formato y dígito verificador
        es_valido, mensaje = validar_rut_chileno(rut)
        if not es_valido:
            raise forms.ValidationError(mensaje)
        
        # Normalizar RUT (sin puntos ni guión)
        rut_normalizado = rut.replace('.', '').replace('-', '')
        
        # Verificar que no esté duplicado
        if Persona.objects.filter(rut=rut_normalizado).exists():
            raise forms.ValidationError('Este RUT ya está registrado en el sistema')
        
        return rut_normalizado
    
    def clean_nombre(self):
        """Valida nombre"""
        nombre = self.cleaned_data.get('nombre')
        
        if not nombre or len(nombre.strip()) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres')
        
        if not nombre.replace(' ', '').isalpha():
            raise forms.ValidationError('El nombre solo debe contener letras y espacios')
        
        return nombre.strip()
    
    def clean_apellido(self):
        """Valida apellido"""
        apellido = self.cleaned_data.get('apellido')
        
        if not apellido or len(apellido.strip()) < 2:
            raise forms.ValidationError('El apellido debe tener al menos 2 caracteres')
        
        if not apellido.replace(' ', '').isalpha():
            raise forms.ValidationError('El apellido solo debe contener letras y espacios')
        
        return apellido.strip()
    
    def clean_edad(self):
        """Valida edad (12-60 años)"""
        edad = self.cleaned_data.get('edad')
        
        if not edad:
            raise forms.ValidationError('La edad es obligatoria')
        
        es_valida, mensaje = validar_edad(edad)
        if not es_valida:
            raise forms.ValidationError(mensaje)
        
        return edad
    
    def clean_direccion(self):
        """Valida dirección"""
        direccion = self.cleaned_data.get('direccion')
        
        if not direccion or len(direccion.strip()) < 5:
            raise forms.ValidationError('La dirección debe tener al menos 5 caracteres')
        
        return direccion.strip()
    
    def clean_contacto(self):
        """Valida teléfono"""
        contacto = self.cleaned_data.get('contacto')
        
        if not contacto:
            raise forms.ValidationError('El teléfono es obligatorio')
        
        es_valido, mensaje = validar_telefono(contacto)
        if not es_valido:
            raise forms.ValidationError(mensaje)
        
        return contacto
