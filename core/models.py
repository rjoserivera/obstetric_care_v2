from django.db import models

class Persona(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]
    
    Rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    Nombre = models.CharField(max_length=150, verbose_name="Nombre")
    Apellido_Paterno = models.CharField(max_length=150, verbose_name="Apellido Paterno")
    Apellido_Materno = models.CharField(max_length=150, verbose_name="Apellido Materno")
    Sexo = models.CharField(max_length=20, choices=SEXO_CHOICES, verbose_name="Sexo")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    Telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    Direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")
    Comuna = models.CharField(max_length=100, blank=True, verbose_name="Comuna")
    Email = models.EmailField(blank=True, verbose_name="Email")
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno} - {self.Rut}"