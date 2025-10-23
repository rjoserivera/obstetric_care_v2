from django.contrib import admin
from .models import Admision

################
# Admin: Admision
# Descripción: Registro de admisiones en el administrador
################
@admin.register(Admision)
class AdmisionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'Previcion', 'estado', 'fecha_admision')
    search_fields = ('persona__Rut', 'persona__Nombre')
    list_filter = ('estado', 'Previcion', 'fecha_admision')
    readonly_fields = ('fecha_admision', 'fecha_actualizacion')
    fieldsets = (
        ('Persona', {
            'fields': ('persona',)
        }),
        ('Datos de Admisión', {
            'fields': ('Previcion', 'estado')
        }),
        ('Sistema', {
            'fields': ('fecha_admision', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )