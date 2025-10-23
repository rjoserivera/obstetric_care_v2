# Temporalmente deshabilitado - Revisar nombres de campos
# from django.contrib import admin
# from .models import Paciente, ControlPrenatal
#
# ################
# # Admin: Paciente
# # Descripción: Registro de pacientes en el administrador
# ################
# @admin.register(Paciente)
# class PacienteAdmin(admin.ModelAdmin):
#     list_display = ('numero_ficha', 'persona', 'embarazos_previos', 'fecha_creacion')
#     search_fields = ('numero_ficha', 'persona__rut', 'persona__nombre')
#     list_filter = ('hipertension', 'diabetes', 'diabetes_gestacional', 'fecha_creacion')
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
#
#
# ################
# # Admin: ControlPrenatal
# # Descripción: Registro de controles prenatales en el administrador
# ################
# @admin.register(ControlPrenatal)
# class ControlPrenatalAdmin(admin.ModelAdmin):
#     list_display = ('paciente', 'fecha_control', 'semanas_gestacion', 'peso')
#     search_fields = ('paciente__numero_ficha', 'paciente__persona__nombre')
#     list_filter = ('fecha_control', 'semanas_gestacion')
#     readonly_fields = ('fecha_registro',)