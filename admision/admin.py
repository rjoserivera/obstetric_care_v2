from django.contrib import admin
from .models import Admision

################
# Admin: Admision
# Descripción: Registro de admisiones en el administrador
################
@admin.register(Admision)
class AdmisionAdmin(admin.ModelAdmin):
    list_display = ('persona', 'previsión', 'estado', 'fecha_admision')
    search_fields = ('persona__rut', 'persona__nombre')
    list_filter = ('estado', 'previsión', 'fecha_admision')
    readonly_fields = ('fecha_admision', 'fecha_actualizacion')