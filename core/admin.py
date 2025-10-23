from django.contrib import admin
from .models import Persona

################
# Admin: Persona
# Descripción: Registro de personas en el administrador
################
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('Rut', 'Nombre', 'Apellido_Paterno', 'Email', 'Activo')
    search_fields = ('Rut', 'Nombre', 'Apellido_Paterno')
    list_filter = ('Activo', 'fecha_creacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Datos Personales', {
            'fields': ('Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno', 'Sexo')
        }),
        ('Contacto', {
            'fields': ('Telefono', 'Direccion', 'Email')
        }),
        ('Sistema', {
            'fields': ('Activo', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )