################
# FORMULARIO: Crear Perfil
# Ubicación: apps/personal/Forms/Form_crear_perfil.py
################

from django import forms
from django.contrib.auth.models import User
from personal.models import Perfil
from utilities.validadores import validar_telefono


class Form_crear_perfil(forms.ModelForm):
    """
    Formulario para crear un nuevo perfil de usuario.
    Vincula un usuario de Django con un rol específico.
    Usado por: Administrativo
    """
    
    # Campo para seleccionar usuario existente
    usuario = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__isnull=True),  # Solo sin perfil asignado
        label='Usuario',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        help_text='Seleccione un usuario existente que aún no tenga perfil asignado'
    )
    
    class Meta:
        model = Perfil
        fields = ['usuario', 'rol', 'especialidad', 'departamento', 'telefono', 'imagen']
        widgets = {
            'rol': forms.Select(attrs={
                'class': 'form-control',
            }),
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
        }
        labels = {
            'rol': 'Rol',
            'especialidad': 'Especialidad',
            'departamento': 'Departamento/Área',
            'telefono': 'Teléfono de Contacto',
            'imagen': 'Foto de Perfil',
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
