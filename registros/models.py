################
# MODELO: Observacion (Registros)
# Descripción: Notas y observaciones clínicas
# v0.2: Agregada IMAGEN, campos de auditoría
################

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from pacientes.models import Paciente


class Observacion(models.Model):
    """
    Observación clínica registrada por Matrona o Médico.
    Puede incluir una imagen anexa (ej: ecografía, resultado de examen).
    """
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='observaciones',
        verbose_name="Paciente"
    )
    
    texto = models.TextField(
        verbose_name="Observación"
    )
    
    # NUEVO EN V0.2: Imagen anexa
    imagen = models.ImageField(
        upload_to='observaciones/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Imagen Anexa",
        help_text="Ej: Ecografía, resultado de examen (JPG, PNG - máx 2MB)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='observaciones_creadas',
        verbose_name="Registrado por"
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
        related_name='observaciones_modificadas',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['paciente', '-created_at']),
        ]
    
    def __str__(self):
        return f"Observación {self.created_at.strftime('%d/%m/%Y')} - {self.paciente.numero_ficha}"


################
# MODELO: Patologia (Registros)
# Descripción: Patologías diagnosticadas
# v0.2: Agregada IMAGEN, campos de auditoría, estado
################

class Patologia(models.Model):
    """
    Patología diagnosticada en el paciente.
    Puede incluir imagen de referencia (ej: resultado de laboratorio).
    Relación M:N con Paciente (un paciente puede tener múltiples patologías).
    """
    
    NIVEL_RIESGO_CHOICES = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('resuelta', 'Resuelta'),
        ('inactiva', 'Inactiva'),
    ]
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='patologias',
        verbose_name="Paciente"
    )
    
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de Patología"
    )
    
    codigo_cie_10 = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código CIE-10"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    
    # NUEVO EN V0.2: Imagen de referencia
    imagen = models.ImageField(
        upload_to='patologias/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Imagen de Referencia",
        help_text="Ej: Resultado de laboratorio, diagnóstico por imagen (JPG, PNG - máx 2MB)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    # Nivel de riesgo
    nivel_riesgo = models.CharField(
        max_length=20,
        choices=NIVEL_RIESGO_CHOICES,
        default='medio',
        verbose_name="Nivel de Riesgo"
    )
    
    # Protocolo de seguimiento
    protocolo_seguimiento = models.TextField(
        blank=True,
        null=True,
        verbose_name="Protocolo de Seguimiento"
    )
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activa',
        verbose_name="Estado"
    )
    
    # Fecha de diagnóstico
    fecha_diagnostico = models.DateField(
        verbose_name="Fecha de Diagnóstico"
    )
    
    # Fecha de resolución
    fecha_resolucion = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Resolución"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    diagnosticado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patologias_diagnosticadas',
        verbose_name="Diagnosticado por"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='patologias_creadas',
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
        related_name='patologias_modificadas',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Patología"
        verbose_name_plural = "Patologías"
        ordering = ['-fecha_diagnostico']
        indexes = [
            models.Index(fields=['paciente', 'estado']),
            models.Index(fields=['nivel_riesgo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.paciente.numero_ficha} ({self.get_estado_display()})"
    
    def get_color_riesgo(self):
        """Retorna color Bootstrap según nivel de riesgo"""
        colores = {
            'bajo': 'success',
            'medio': 'warning',
            'alto': 'danger',
            'critico': 'dark',
        }
        return colores.get(self.nivel_riesgo, 'secondary')


################
# MODELO: Procedimiento (Registros)
# Descripción: Procedimientos realizados
# v0.2: Agregada IMAGEN, campos de auditoría
################

class Procedimiento(models.Model):
    """
    Procedimiento médico realizado al paciente.
    Usualmente registrado por TENS pero puede ser por Matrona o Médico.
    Puede incluir imagen de evidencia.
    """
    
    TIPO_PROCEDIMIENTO_CHOICES = [
        ('inyeccion', 'Inyección'),
        ('extraccion', 'Extracción de sangre'),
        ('sutura', 'Sutura'),
        ('curacion', 'Curación'),
        ('cateterismo', 'Cateterismo'),
        ('sonda', 'Colocación de sonda'),
        ('medicacion', 'Medicación'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='procedimientos',
        verbose_name="Paciente"
    )
    
    tipo_procedimiento = models.CharField(
        max_length=50,
        choices=TIPO_PROCEDIMIENTO_CHOICES,
        verbose_name="Tipo de Procedimiento"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )
    
    # NUEVO EN V0.2: Imagen de evidencia
    imagen = models.ImageField(
        upload_to='procedimientos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Foto de Evidencia",
        help_text="Evidencia fotográfica del procedimiento realizado (JPG, PNG - máx 2MB)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    # Fecha y hora del procedimiento
    fecha_procedimiento = models.DateTimeField(
        verbose_name="Fecha y Hora del Procedimiento"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='realizado',
        verbose_name="Estado"
    )
    
    # Material utilizado
    material_utilizado = models.TextField(
        blank=True,
        null=True,
        verbose_name="Material Utilizado"
    )
    
    # Observaciones post-procedimiento
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
        related_name='procedimientos_realizados',
        verbose_name="Realizado por"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='procedimientos_creados',
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
        related_name='procedimientos_modificados',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        ordering = ['-fecha_procedimiento']
        indexes = [
            models.Index(fields=['paciente', '-fecha_procedimiento']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_procedimiento_display()} - {self.paciente.numero_ficha} ({self.fecha_procedimiento.strftime('%d/%m/%Y')})"


################
# MODELO: Medicamento (Registros)
# Descripción: Medicamentos administrados
# v0.2: Campos de auditoría
################

class Medicamento(models.Model):
    """
    Registro de medicamento administrado al paciente.
    Usualmente aplicado por TENS pero puede ser por Matrona o Médico.
    """
    
    VIA_ADMINISTRACION_CHOICES = [
        ('oral', 'Oral'),
        ('intramuscular', 'Intramuscular'),
        ('intravenosa', 'Intravenosa'),
        ('subcutanea', 'Subcutánea'),
        ('topica', 'Tópica'),
        ('rectal', 'Rectal'),
        ('vaginal', 'Vaginal'),
        ('otra', 'Otra'),
    ]
    
    ESTADO_CHOICES = [
        ('prescrito', 'Prescrito'),
        ('administrado', 'Administrado'),
        ('no_administrado', 'No Administrado'),
    ]
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name="Paciente"
    )
    
    nombre_medicamento = models.CharField(
        max_length=255,
        verbose_name="Nombre del Medicamento"
    )
    
    dosis = models.CharField(
        max_length=100,
        verbose_name="Dosis",
        help_text="Ej: 500mg, 1 comprimido"
    )
    
    via_administracion = models.CharField(
        max_length=50,
        choices=VIA_ADMINISTRACION_CHOICES,
        verbose_name="Vía de Administración"
    )
    
    frecuencia = models.CharField(
        max_length=100,
        verbose_name="Frecuencia",
        help_text="Ej: Cada 8 horas, 2 veces al día"
    )
    
    duracion_dias = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Duración (días)"
    )
    
    indicacion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Indicación Médica"
    )
    
    # Fecha de prescripción
    fecha_prescripcion = models.DateField(
        verbose_name="Fecha de Prescripción"
    )
    
    # Fecha de administración
    fecha_administracion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha y Hora de Administración"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='prescrito',
        verbose_name="Estado"
    )
    
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    prescrito_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='medicamentos_prescritos',
        verbose_name="Prescrito por"
    )
    
    administrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicamentos_administrados',
        verbose_name="Administrado por"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='medicamentos_creados',
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
        related_name='medicamentos_modificados',
        verbose_name="Modificado por"
    )
    
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['-fecha_prescripcion']
        indexes = [
            models.Index(fields=['paciente', 'estado']),
            models.Index(fields=['fecha_administracion']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente.numero_ficha}"
    
    def get_duracion_total(self):
        """Retorna la duración formateada"""
        if self.duracion_dias:
            return f"{self.duracion_dias} días"
        return "Indefinida"