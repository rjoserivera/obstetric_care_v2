from django.contrib import admin
from .models import Persona

################
# Admin: Persona
# Descripción: Registro de personas en el administrador
################
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'edad', 'email')
    search_fields = ('rut', 'nombre', 'apellido')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')