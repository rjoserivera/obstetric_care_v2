from django.db import models
from django.contrib.auth.models import User
from pacientes.models import Paciente

################
# Modelo: Observacion
# Descripción: Registro de observaciones médicas
################
class Observacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='observaciones')
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Médico'})
    texto = models.TextField()
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Observación {self.fecha_creacion} - {self.paciente.numero_ficha}"


################
# Modelo: Patologia
# Descripción: Patologías registradas del paciente
################
class Patologia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='patologias')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Médico'})
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Patología"
        verbose_name_plural = "Patologías"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre} - {self.paciente.numero_ficha}"


################
# Modelo: Procedimiento
# Descripción: Procedimientos realizados por TENS
################
class Procedimiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='procedimientos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    realizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'TENS'})
    
    fecha_procedimiento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        ordering = ['-fecha_procedimiento']
    
    def __str__(self):
        return f"{self.nombre} - {self.paciente.numero_ficha}"


################
# Modelo: Medicamento
# Descripción: Medicamentos administrados al paciente
################
class Medicamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='medicamentos')
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=50)
    administrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'TENS'})
    
    fecha_administracion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['-fecha_administracion']
    
    def __str__(self):
        return f"{self.nombre} - {self.paciente.numero_ficha}"