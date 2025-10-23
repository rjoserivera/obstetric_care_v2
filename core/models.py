################
# MODELO: Persona (Core - Base)
# Descripción: Registro base de cualquier persona (madre)
# v0.2: Agregados campos de auditoría
################

from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    """
    Modelo base para cualquier persona en el sistema.
    Usada para pacientes (madres) en módulo de obstetricia.
    """
    
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="RUT",
        help_text="Formato: XX.XXX.XXX-X"
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre"
    )
    apellido = models.CharField(
        max_length=255,
        verbose_name="Apellido"
    )
    edad = models.IntegerField(
        verbose_name="Edad",
        help_text="Rango permitido: 12-60 años"
    )
    direccion = models.TextField(
        verbose_name="Dirección"
    )
    contacto = models.CharField(
        max_length=20,
        verbose_name="Teléfono de Contacto",
        help_text="Formato: +56912345678 o 912345678"
    )
    
    # AUDITORÍA (Nuevo en v0.2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='personas_creadas',
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
        related_name='personas_modificadas',
        verbose_name="Modificado por"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    # ESTADO (Nuevo en v0.2 - Soft Delete)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
        ],
        default='activo',
        verbose_name="Estado"
    )
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rut']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"
    
    def get_full_name(self):
        """Retorna nombre completo"""
        return f"{self.nombre} {self.apellido}"