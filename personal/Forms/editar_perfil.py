################
# FORMULARIO: Editar Perfil
# Ubicación: apps/personal/Forms/Form_editar_perfil.py
################

from django import forms
from personal.models import Perfil
from utilities.validadores import validar_telefono


class Form_editar_perfil(forms.ModelForm):
    """
    Formulario para editar datos de un perfil existente.
    Incluye cambio de estado (activo/inactivo).
    Usado por: Administrativo
    """
    
    class Meta:
        model = Perfil
        fields = ['especialidad', 'departamento', 'telefono', 'imagen', 'estado']
        widgets = {
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Obstetricia, Ginecología',
                'maxlength': '100'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Obstetricia, Urgencias',
                'maxlength': '100'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +56912345678 o 912345678',
                'maxlength': '20'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB en bytes
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'especialidad': 'Especialidad',
            'departamento': 'Departamento/Área',
            'telefono': 'Teléfono de Contacto',
            'imagen': 'Foto de Perfil',
            'estado': 'Estado',
        }
    
    def clean_telefono(self):
        """Valida teléfono si está presente"""
        telefono = self.cleaned_data.get('telefono')
        
        if telefono:  # Es opcional
            es_valido, mensaje = validar_telefono(telefono)
            if not es_valido:
                raise forms.ValidationError(mensaje)
        
        return telefono
    
    def clean_imagen(self):
        """Valida imagen (tamaño y formato)"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            # Validar tamaño (máx 2MB)
            if imagen.size > 2097152:  # 2MB en bytes
                raise forms.ValidationError('La imagen no puede superar 2MB de tamaño')
            
            # Validar formato
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo se permiten imágenes JPG o PNG')
        
        return imagen
