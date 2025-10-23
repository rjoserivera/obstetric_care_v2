################
# MODELO: Perfil (Personal - Roles y Usuarios)
# Descripción: Perfil de usuario con rol personalizado
# v0.2: Nuevo modelo personalizado (NO Django Groups)
#       Con imagen, especialidad, departamento, teléfono, estado
################

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Perfil(models.Model):
    """
    Perfil personalizado de usuario con roles específicos.
    No usa Django Groups - permite mayor personalización.
    
    Roles disponibles:
    - administrativo: Gestión general del sistema
    - matrona: Profesional de enfermería obstétrica
    - medico: Médico especialista
    - tens: Técnico en enfermería
    """
    
    ROL_CHOICES = [
        ('administrativo', 'Administrativo'),
        ('matrona', 'Matrona'),
        ('medico', 'Médico'),
        ('tens', 'TENS'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    # Relación con User de Django (autenticación)
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Usuario"
    )
    
    # Rol principal
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        verbose_name="Rol"
    )
    
    # NUEVO EN V0.2: Imagen de perfil
    imagen = models.ImageField(
        upload_to='perfiles/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
        help_text="Formatos permitidos: JPG, PNG (máx 2MB)",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    
    # Campos personalizados (Nuevo en v0.2)
    especialidad = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Especialidad",
        help_text="Ej: Obstetricia, Ginecología, Pediatría"
    )
    
    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Departamento/Área",
        help_text="Ej: Obstetricia, Cuidados Intensivos, Urgencias"
    )
    
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono de Contacto",
        help_text="Formato: +56912345678 o 912345678"
    )
    
    # Estado del perfil
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo',
        verbose_name="Estado"
    )
    
    # Auditoría (Nuevo en v0.2)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rol']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"
    
    def get_rol_display_formal(self):
        """Retorna el rol en formato formal"""
        rol_formal = {
            'administrativo': 'Administrativo/a',
            'matrona': 'Matrona',
            'medico': 'Médico/a',
            'tens': 'TENS',
        }
        return rol_formal.get(self.rol, self.rol)
    
    def tiene_permiso(self, accion):
        """
        Verifica si el perfil tiene permiso para una acción.
        
        Uso:
            if perfil.tiene_permiso('crear_paciente'):
                # hacer algo
        
        Retorna: Boolean
        """
        permisos = {
            'crear_paciente': ['administrativo', 'matrona', 'medico'],
            'ver_ficha': ['administrativo', 'matrona', 'medico'],
            'editar_antecedentes': ['administrativo', 'matrona', 'medico'],
            'diagnosticar': ['administrativo', 'matrona', 'medico'],
            'registrar_procedimiento': ['administrativo', 'matrona', 'medico', 'tens'],
            'aplicar_medicamento': ['administrativo', 'matrona', 'medico', 'tens'],
        }
        
        acciones_permitidas = permisos.get(accion, [])
        return self.rol in acciones_permitidas
    
    @property
    def imagen_url(self):
        """Retorna URL de la imagen o imagen por defecto"""
        if self.imagen:
            return self.imagen.url
        else:
            # Retorna imagen por defecto según rol
            imagenes_default = {
                'administrativo': '/static/img/default_admin.png',
                'matrona': '/static/img/default_matrona.png',
                'medico': '/static/img/default_medico.png',
                'tens': '/static/img/default_tens.png',
            }
            return imagenes_default.get(self.rol, '/static/img/default_user.png')