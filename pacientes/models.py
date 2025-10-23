################
# MODELO: Paciente (Pacientes - Ficha Clínica)
# Descripción: Ficha clínica de paciente (madre embarazada)
# v0.2: Agregados campos de auditoría y estado
################

from django.db import models
from django.contrib.auth.models import User
from core.models import Persona


class Paciente(models.Model):
    """
    Ficha clínica de paciente embarazada.
    Vinculada a una Persona (madre).
    """
    
    ESTADO_CIVIL_CHOICES = [
        ('soltera', 'Soltera'),
        ('casada', 'Casada'),
        ('divorciada', 'Divorciada'),
        ('viuda', 'Viuda'),
        ('conviviente', 'Conviviente'),
    ]
    
    PREVISION_CHOICES = [
        ('fonasa', 'FONASA'),
        ('isapre', 'ISAPRE'),
        ('privado', 'Privado'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_PACIENTE_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('alta', 'Alta'),
        ('fallecimiento', 'Fallecimiento'),
    ]
    
    # Relación con Persona
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='paciente',
        verbose_name="Persona"
    )
    
    # Identificadores
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Ficha",
        help_text="Se genera automáticamente. Formato: FAM-YYYY-XXXXX"
    )
    
    # Información clínica básica
    edad = models.IntegerField(
        verbose_name="Edad",
        help_text="Rango permitido: 12-60 años"
    )
    
    estado_civil = models.CharField(
        max_length=20,
        choices=ESTADO_CIVIL_CHOICES,
        verbose_name="Estado Civil"
    )
    
    prevision = models.CharField(
        max_length=20,
        choices=PREVISION_CHOICES,
        verbose_name="Previsión de Salud"
    )
    
    # Antecedentes obstétricos
    embarazos_previos = models.IntegerField(
        default=0,
        verbose_name="Embarazos Previos"
    )
    
    partos_previos = models.IntegerField(
        default=0,
        verbose_name="Partos Previos"
    )
    
    abortos_previos = models.IntegerField(
        default=0,
        verbose_name="Abortos Previos"
    )
    
    # Patologías (Deprecated - usar tabla Patologia en registros)
    hipertension = models.BooleanField(
        default=False,
        verbose_name="Hipertensión"
    )
    
    diabetes = models.BooleanField(
        default=False,
        verbose_name="Diabetes"
    )
    
    diabetes_gestacional = models.BooleanField(
        default=False,
        verbose_name="Diabetes Gestacional"
    )
    
    otras_patologias = models.TextField(
        blank=True,
        null=True,
        verbose_name="Otras Patologías"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pacientes_creados',
        verbose_name="Creado por"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_modificados',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    # ESTADO (Nuevo en v0.2 - Soft Delete)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_PACIENTE_CHOICES,
        default='activo',
        verbose_name="Estado del Paciente"
    )
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['numero_ficha']),
            models.Index(fields=['estado']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.persona.get_full_name()}"
    
    def get_edad_gestacional(self):
        """Calcula edad gestacional aproximada (requiere datos de controles)"""
        # Implementar después con modelo ControlPrenatal
        pass
    
    def get_patologias_activas(self):
        """Retorna patologías activas del paciente"""
        return self.patologias.filter(estado='activo')


################
# MODELO: ControlPrenatal
# Descripción: Registro de control prenatal
# Nuevo en v0.2
################

class ControlPrenatal(models.Model):
    """
    Registro de cada control prenatal realizado.
    Vinculado a un Paciente.
    """
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='controles_prenatales',
        verbose_name="Paciente"
    )
    
    # Datos del control
    fecha_control = models.DateField(
        verbose_name="Fecha del Control"
    )
    
    semanas_gestacion = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Semanas de Gestación"
    )
    
    # Mediciones
    peso = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Peso (kg)"
    )
    
    presion_sistolica = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Presión Sistólica"
    )
    
    presion_diastolica = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Presión Diastólica"
    )
    
    frecuencia_cardiaca = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Frecuencia Cardíaca (bpm)"
    )
    
    glucemia = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Glucemia (mg/dL)"
    )
    
    # Observaciones
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    realizado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='controles_realizados',
        verbose_name="Realizado por"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='controles_creados',
        verbose_name="Registrado por"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='controles_modificados',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Control Prenatal"
        verbose_name_plural = "Controles Prenatales"
        ordering = ['-fecha_control']
        indexes = [
            models.Index(fields=['paciente', '-fecha_control']),
        ]
    
    def __str__(self):
        return f"Control {self.fecha_control} - {self.paciente.numero_ficha}"
    
    def get_presion(self):
        """Retorna presión formateada"""
        if self.presion_sistolica and self.presion_diastolica:
            return f"{self.presion_sistolica}/{self.presion_diastolica}"
        return "N/D"


################
# MODELO: AntecedentesClinico
# Descripción: Antecedentes clínicos del paciente
# v0.2: Agregados campos de auditoría
################

class AntecedentesClinico(models.Model):
    """
    Registro de antecedentes clínicos del paciente.
    Puede ser: control prenatal, embarazo anterior, alergia, etc.
    """
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('control_prenatal', 'Control Prenatal'),
        ('embarazo_anterior', 'Embarazo Anterior'),
        ('patologia', 'Patología'),
        ('medicamento', 'Medicamento'),
        ('alergia', 'Alergia'),
        ('cirugia', 'Cirugía'),
        ('otro', 'Otro'),
    ]
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='antecedentes',
        verbose_name="Paciente"
    )
    
    tipo_dato = models.CharField(
        max_length=50,
        choices=TIPO_ANTECEDENTE_CHOICES,
        verbose_name="Tipo de Antecedente"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='antecedentes_registrados',
        verbose_name="Registrado por"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='antecedentes_modificados',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Antecedente Clínico"
        verbose_name_plural = "Antecedentes Clínicos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['paciente', 'tipo_dato']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_dato_display()} - {self.paciente.numero_ficha}"