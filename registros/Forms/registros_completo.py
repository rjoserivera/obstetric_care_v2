################
# FORMULARIOS: Registros
# Descripción: Formularios para observaciones, patologías, procedimientos y medicamentos
# v0.2: Con imágenes y validaciones completas
################

from django import forms
from django.utils import timezone
from registros.models import Observacion, Patologia, Procedimiento, Medicamento


# ====================================================================
# OBSERVACIÓN
# ====================================================================

class Form_agregar_observacion(forms.ModelForm):
    """
    Formulario para agregar una nueva observación clínica.
    Permite anexar imagen (ecografía, resultado examen, etc).
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = Observacion
        fields = ['texto', 'imagen']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Registre la observación clínica',
                'rows': '4'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
        }
        labels = {
            'texto': 'Observación',
            'imagen': 'Imagen Anexa (Ecografía, Examen, etc)',
        }
    
    def clean_texto(self):
        """Valida texto"""
        texto = self.cleaned_data.get('texto')
        
        if not texto or len(texto.strip()) < 5:
            raise forms.ValidationError('La observación debe tener al menos 5 caracteres')
        
        return texto.strip()
    
    def clean_imagen(self):
        """Valida imagen (tamaño y formato)"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


class Form_editar_observacion(forms.ModelForm):
    """
    Formulario para editar una observación existente.
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = Observacion
        fields = ['texto', 'imagen']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Registre la observación clínica',
                'rows': '4'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
        }
        labels = {
            'texto': 'Observación',
            'imagen': 'Imagen Anexa',
        }
    
    def clean_texto(self):
        """Valida texto"""
        texto = self.cleaned_data.get('texto')
        
        if not texto or len(texto.strip()) < 5:
            raise forms.ValidationError('La observación debe tener al menos 5 caracteres')
        
        return texto.strip()
    
    def clean_imagen(self):
        """Valida imagen"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


# ====================================================================
# PATOLOGÍA
# ====================================================================

class Form_agregar_patologia(forms.ModelForm):
    """
    Formulario para agregar una nueva patología diagnosticada.
    Permite anexar imagen de diagnóstico.
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = Patologia
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 'imagen', 
                  'nivel_riesgo', 'protocolo_seguimiento', 'fecha_diagnostico']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la patología',
                'maxlength': '100'
            }),
            'codigo_cie_10': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: O99.8',
                'maxlength': '10'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada',
                'rows': '3'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
            'nivel_riesgo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'protocolo_seguimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Protocolo a seguir',
                'rows': '3'
            }),
            'fecha_diagnostico': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'nombre': 'Nombre de Patología',
            'codigo_cie_10': 'Código CIE-10',
            'descripcion': 'Descripción',
            'imagen': 'Imagen de Diagnóstico',
            'nivel_riesgo': 'Nivel de Riesgo',
            'protocolo_seguimiento': 'Protocolo de Seguimiento',
            'fecha_diagnostico': 'Fecha de Diagnóstico',
        }
    
    def clean_nombre(self):
        """Valida nombre"""
        nombre = self.cleaned_data.get('nombre')
        
        if not nombre or len(nombre.strip()) < 2:
            raise forms.ValidationError('El nombre debe tener al menos 2 caracteres')
        
        return nombre.strip()
    
    def clean_fecha_diagnostico(self):
        """Valida fecha"""
        fecha = self.cleaned_data.get('fecha_diagnostico')
        
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha no puede ser futura')
        
        return fecha
    
    def clean_imagen(self):
        """Valida imagen"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


class Form_editar_patologia(forms.ModelForm):
    """
    Formulario para editar una patología existente.
    Usado por: Matrona, Médico
    """
    
    class Meta:
        model = Patologia
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 'imagen', 
                  'nivel_riesgo', 'protocolo_seguimiento', 'estado', 'fecha_resolucion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la patología',
                'maxlength': '100'
            }),
            'codigo_cie_10': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: O99.8',
                'maxlength': '10'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada',
                'rows': '3'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
            'nivel_riesgo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'protocolo_seguimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Protocolo a seguir',
                'rows': '3'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha_resolucion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'nombre': 'Nombre de Patología',
            'codigo_cie_10': 'Código CIE-10',
            'descripcion': 'Descripción',
            'imagen': 'Imagen de Diagnóstico',
            'nivel_riesgo': 'Nivel de Riesgo',
            'protocolo_seguimiento': 'Protocolo de Seguimiento',
            'estado': 'Estado',
            'fecha_resolucion': 'Fecha de Resolución',
        }
    
    def clean_imagen(self):
        """Valida imagen"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


# ====================================================================
# PROCEDIMIENTO
# ====================================================================

class Form_registrar_procedimiento(forms.ModelForm):
    """
    Formulario para registrar un nuevo procedimiento.
    Permite anexar foto de evidencia.
    Usado por: Matrona, Médico, TENS
    """
    
    class Meta:
        model = Procedimiento
        fields = ['tipo_procedimiento', 'descripcion', 'fecha_procedimiento', 
                  'material_utilizado', 'imagen', 'observaciones']
        widgets = {
            'tipo_procedimiento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del procedimiento',
                'rows': '3'
            }),
            'fecha_procedimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'material_utilizado': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Material usado',
                'rows': '2'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones post-procedimiento',
                'rows': '3'
            }),
        }
        labels = {
            'tipo_procedimiento': 'Tipo de Procedimiento',
            'descripcion': 'Descripción',
            'fecha_procedimiento': 'Fecha y Hora',
            'material_utilizado': 'Material Utilizado',
            'imagen': 'Foto de Evidencia',
            'observaciones': 'Observaciones',
        }
    
    def clean_fecha_procedimiento(self):
        """Valida fecha"""
        fecha = self.cleaned_data.get('fecha_procedimiento')
        
        if fecha and fecha > timezone.now():
            raise forms.ValidationError('La fecha no puede ser futura')
        
        return fecha
    
    def clean_imagen(self):
        """Valida imagen"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


class Form_editar_procedimiento(forms.ModelForm):
    """
    Formulario para editar un procedimiento existente.
    Usado por: Matrona, Médico, TENS
    """
    
    class Meta:
        model = Procedimiento
        fields = ['tipo_procedimiento', 'descripcion', 'fecha_procedimiento', 
                  'material_utilizado', 'imagen', 'estado', 'observaciones']
        widgets = {
            'tipo_procedimiento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del procedimiento',
                'rows': '3'
            }),
            'fecha_procedimiento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'material_utilizado': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Material usado',
                'rows': '2'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/png',
                'data-max-size': '2097152'  # 2MB
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': '3'
            }),
        }
        labels = {
            'tipo_procedimiento': 'Tipo de Procedimiento',
            'descripcion': 'Descripción',
            'fecha_procedimiento': 'Fecha y Hora',
            'material_utilizado': 'Material Utilizado',
            'imagen': 'Foto de Evidencia',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }
    
    def clean_imagen(self):
        """Valida imagen"""
        imagen = self.cleaned_data.get('imagen')
        
        if imagen:
            if imagen.size > 2097152:  # 2MB
                raise forms.ValidationError('La imagen no puede superar 2MB')
            
            formatos_permitidos = ['image/jpeg', 'image/png']
            if imagen.content_type not in formatos_permitidos:
                raise forms.ValidationError('Solo JPG o PNG permitidos')
        
        return imagen


# ====================================================================
# MEDICAMENTO
# ====================================================================

class Form_prescribir_medicamento(forms.ModelForm):
    """
    Formulario para prescribir un nuevo medicamento.
    Usado por: Médico, Matrona
    """
    
    class Meta:
        model = Medicamento
        fields = ['nombre_medicamento', 'dosis', 'via_administracion', 
                  'frecuencia', 'duracion_dias', 'indicacion', 'fecha_prescripcion']
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento',
                'maxlength': '255'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 1 comprimido',
                'maxlength': '100'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-control',
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas, 2 veces al día',
                'maxlength': '100'
            }),
            'duracion_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Días',
                'min': '1',
                'type': 'number'
            }),
            'indicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Indicación médica',
                'rows': '3'
            }),
            'fecha_prescripcion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'nombre_medicamento': 'Medicamento',
            'dosis': 'Dosis',
            'via_administracion': 'Vía de Administración',
            'frecuencia': 'Frecuencia',
            'duracion_dias': 'Duración (días)',
            'indicacion': 'Indicación Médica',
            'fecha_prescripcion': 'Fecha de Prescripción',
        }
    
    def clean_fecha_prescripcion(self):
        """Valida fecha"""
        fecha = self.cleaned_data.get('fecha_prescripcion')
        
        if fecha and fecha > timezone.now().date():
            raise forms.ValidationError('La fecha no puede ser futura')
        
        return fecha


class Form_administrar_medicamento(forms.ModelForm):
    """
    Formulario para registrar administración de medicamento.
    Usado por: TENS, Matrona, Médico
    """
    
    class Meta:
        model = Medicamento
        fields = ['estado', 'fecha_administracion', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha_administracion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones de la administración',
                'rows': '3'
            }),
        }
        labels = {
            'estado': 'Estado',
            'fecha_administracion': 'Fecha y Hora de Administración',
            'observaciones': 'Observaciones',
        }
    
    def clean_fecha_administracion(self):
        """Valida fecha"""
        fecha = self.cleaned_data.get('fecha_administracion')
        
        if fecha and fecha > timezone.now():
            raise forms.ValidationError('La fecha no puede ser futura')
        
        return fecha


class Form_editar_medicamento(forms.ModelForm):
    """
    Formulario para editar un medicamento.
    Usado por: Médico, Matrona
    """
    
    class Meta:
        model = Medicamento
        fields = ['nombre_medicamento', 'dosis', 'via_administracion', 
                  'frecuencia', 'duracion_dias', 'indicacion', 'estado', 'observaciones']
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento',
                'maxlength': '255'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 500mg, 1 comprimido',
                'maxlength': '100'
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-control',
            }),
            'frecuencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cada 8 horas, 2 veces al día',
                'maxlength': '100'
            }),
            'duracion_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Días',
                'min': '1',
                'type': 'number'
            }),
            'indicacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Indicación médica',
                'rows': '3'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones',
                'rows': '3'
            }),
        }
        labels = {
            'nombre_medicamento': 'Medicamento',
            'dosis': 'Dosis',
            'via_administracion': 'Vía de Administración',
            'frecuencia': 'Frecuencia',
            'duracion_dias': 'Duración (días)',
            'indicacion': 'Indicación Médica',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }
