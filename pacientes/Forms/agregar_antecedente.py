################
# FORMULARIO: Agregar Antecedente Clínico
# Ubicación: apps/pacientes/Forms/Form_agregar_antecedente.py
################

from django import forms
from pacientes.models import AntecedentesClinico


class Form_agregar_antecedente(forms.ModelForm):
    """
    Formulario para agregar un nuevo antecedente clínico.
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = AntecedentesClinico
        fields = ['tipo_dato', 'descripcion']
        widgets = {
            'tipo_dato': forms.Select(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el antecedente detalladamente',
                'rows': '4'
            }),
        }
        labels = {
            'tipo_dato': 'Tipo de Antecedente',
            'descripcion': 'Descripción',
        }
    
    def clean_descripcion(self):
        """Valida descripción"""
        descripcion = self.cleaned_data.get('descripcion')
        
        if not descripcion or len(descripcion.strip()) < 5:
            raise forms.ValidationError('La descripción debe tener al menos 5 caracteres')
        
        return descripcion.strip()
