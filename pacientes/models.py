from django.db import models
from core.models import Persona

################
# Modelo: Paciente
# Descripción: Ficha clínica de paciente (madre)
################
class Paciente(models.Model):
    ESTADO_CIVIL_CHOICES = [
        ('Soltera', 'Soltera'),
        ('Casada', 'Casada'),
        ('Divorciada', 'Divorciada'),
        ('Viuda', 'Viuda'),
        ('Conviviente', 'Conviviente'),
    ]
    
    PREVISION_CHOICES = [
        ('FONASA', 'FONASA'),
        ('ISAPRE', 'ISAPRE'),
        ('Privado', 'Privado'),
        ('Otro', 'Otro'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='paciente')
    numero_ficha = models.CharField(max_length=20, unique=True, verbose_name="Número de Ficha")
    
    Edad = models.IntegerField(verbose_name="Edad")
    Estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, verbose_name="Estado Civil")
    Previcion = models.CharField(max_length=20, choices=PREVISION_CHOICES, verbose_name="Previsión")
    
    # Antecedentes obstétricos
    embarazos_previos = models.IntegerField(default=0, verbose_name="Embarazos Previos")
    partos_previos = models.IntegerField(default=0, verbose_name="Partos Previos")
    abortos_previos = models.IntegerField(default=0, verbose_name="Abortos Previos")
    
    # Patologías
    hipertension = models.BooleanField(default=False, verbose_name="Hipertensión")
    diabetes = models.BooleanField(default=False, verbose_name="Diabetes")
    diabetes_gestacional = models.BooleanField(default=False, verbose_name="Diabetes Gestacional")
    otras_patologias = models.TextField(blank=True, null=True, verbose_name="Otras Patologías")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.persona.Nombre} {self.persona.Apellido_Paterno}"


################
# Modelo: ControlPrenatal
# Descripción: Registro de controles prenatales
################
class ControlPrenatal(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='controles', verbose_name="Paciente")
    fecha_control = models.DateField(verbose_name="Fecha de Control")
    semanas_gestacion = models.IntegerField(verbose_name="Semanas de Gestación")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    presion = models.CharField(max_length=20, blank=True, verbose_name="Presión")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Control Prenatal"
        verbose_name_plural = "Controles Prenatales"
        ordering = ['-fecha_control']
    
    def __str__(self):
        return f"Control {self.fecha_control} - {self.paciente.numero_ficha}"