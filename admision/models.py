from django.db import models
from core.models import Persona

################
# Modelo: Admision
# Descripción: Registro de admisión de persona
################
class Admision(models.Model):
    PREVISION_CHOICES = [
        ('FONASA', 'FONASA'),
        ('ISAPRE', 'ISAPRE'),
        ('Privado', 'Privado'),
        ('Otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='admision')
    Previcion = models.CharField(max_length=20, choices=PREVISION_CHOICES, verbose_name="Previsión")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', verbose_name="Estado")
    
    fecha_admision = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Admisión"
        verbose_name_plural = "Admisiones"
        ordering = ['-fecha_admision']
    
    def __str__(self):
        return f"Admisión - {self.persona.Nombre} {self.persona.Apellido_Paterno}"