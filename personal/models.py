from django.db import models
from django.contrib.auth.models import User
from core.models import Persona

################
# Modelo: Medico
# Descripción: Perfil de médico
################
class Medico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Obstetricia General', 'Obstetricia General'),
        ('Ginecología', 'Ginecología'),
        ('Medicina Materno Fetal', 'Medicina Materno Fetal'),
    ]
    
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='medico', verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES, verbose_name="Especialidad")
    Registro_medico = models.CharField(max_length=100, unique=True, verbose_name="Registro Médico")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.CharField(max_length=20, choices=TURNO_CHOICES, verbose_name="Turno")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
    
    def __str__(self):
        return f"Dr. {self.persona.Nombre} {self.persona.Apellido_Paterno} - {self.Especialidad}"


################
# Modelo: Matrona
# Descripción: Perfil de matrona
################
class Matrona(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Atención del Parto', 'Atención del Parto'),
        ('Control Prenatal', 'Control Prenatal'),
        ('Neonatología', 'Neonatología'),
    ]
    
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='matrona', verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES, verbose_name="Especialidad")
    Registro_medico = models.CharField(max_length=100, unique=True, verbose_name="Registro")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.CharField(max_length=20, choices=TURNO_CHOICES, verbose_name="Turno")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Matrona"
        verbose_name_plural = "Matronas"
    
    def __str__(self):
        return f"Matrona: {self.persona.Nombre} {self.persona.Apellido_Paterno}"


################
# Modelo: TENS
# Descripción: Perfil de TENS
################
class Tens(models.Model):
    NIVEL_CHOICES = [
        ('Preparto', 'Preparto'),
        ('Parto', 'Parto'),
        ('Puerperio', 'Puerperio'),
        ('Neonatología', 'Neonatología'),
    ]
    
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    
    CERTIFICACION_CHOICES = [
        ('SVB', 'Soporte Vital Básico'),
        ('Parto Normal', 'Certificación en Parto Normal'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='tens', verbose_name="Persona")
    Nivel = models.CharField(max_length=100, choices=NIVEL_CHOICES, verbose_name="Nivel")
    Años_experiencia = models.IntegerField(verbose_name="Años de Experiencia")
    Turno = models.CharField(max_length=20, choices=TURNO_CHOICES, verbose_name="Turno")
    Certificaciones = models.CharField(max_length=100, choices=CERTIFICACION_CHOICES, verbose_name="Certificaciones")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "TENS"
        verbose_name_plural = "TENS"
    
    def __str__(self):
        return f"TENS: {self.persona.Nombre} {self.persona.Apellido_Paterno} - {self.Nivel}