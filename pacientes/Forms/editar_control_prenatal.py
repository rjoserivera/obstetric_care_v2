################
# FORMULARIO: Editar Control Prenatal
# Ubicación: apps/pacientes/Forms/Form_editar_control_prenatal.py
################

from django import forms
from django.utils import timezone
from pacientes.models import ControlPrenatal


class Form_editar_control_prenatal(forms.ModelForm):
    """
    Formulario para editar un control prenatal existente.
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = ControlPrenatal
        fields = ['fecha_control', 'semanas_gestacion', 'peso', 
                  'presion_sistolica', 'presion_diastolica', 
                  'frecuencia_cardiaca', 'glucemia', 'observaciones']
        widgets = {
            'fecha_control': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'semanas_gestacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Semanas',
                'min': '1',
                'max': '42',
                'type': 'number'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kg',
                'step': '0.1',
                'type': 'number'
            }),
            'presion_sistolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg',
                'min': '60',
                'max': '220',
                'type': 'number'
            }),
            'presion_diastolica': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mmHg',
                'min': '40',
                'max': '140',
                'type': 'number'
            }),
            'frecuencia_cardiaca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'bpm',
                'min': '40',
                'max': '200',
                'type': 'number'
            }),
            'glucemia': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mg/dL',
                'step': '0.1',
                'type': 'number'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones del control',
                'rows': '3'
            }),
        }
        labels = {
            'fecha_control': 'Fecha del Control',
            'semanas_gestacion': 'Semanas de Gestación',
            'peso': 'Peso (kg)',
            'presion_sistolica': 'Presión Sistólica',
            'presion_diastolica': 'Presión Diastólica',
            'frecuencia_cardiaca': 'Frecuencia Cardíaca (bpm)',
            'glucemia': 'Glucemia (mg/dL)',
            'observaciones': 'Observaciones',
        }
    
    def clean_fecha_control(self):
        """Valida que la fecha no sea futura"""
        fecha = self.cleaned_data.get('fecha_control')
        
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha del control no puede ser futura')
        
        return fecha
    
    def clean_presion_diastolica(self):
        """Valida que presión diastólica sea menor que sistólica"""
        diastolica = self.cleaned_data.get('presion_diastolica')
        sistolica = self.cleaned_data.get('presion_sistolica')
        
        if diastolica and sistolica and diastolica >= sistolica:
            raise forms.ValidationError('La presión diastólica debe ser menor que la sistólica')
        
        return diastolica
