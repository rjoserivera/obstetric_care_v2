# Temporalmente deshabilitado - Revisar nombres de campos
# from django.contrib import admin
# from .models import Observacion, Patologia, Procedimiento, Medicamento
#
# ################
# # Admin: Observacion
# # Descripción: Registro de observaciones médicas en el administrador
# ################
# @admin.register(Observacion)
# class ObservacionAdmin(admin.ModelAdmin):
#     list_display = ('paciente', 'medico', 'fecha_creacion')
#     search_fields = ('paciente__numero_ficha', 'medico__username')
#     list_filter = ('fecha_creacion',)
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
#
#
# ################
# # Admin: Patologia
# # Descripción: Registro de patologías en el administrador
# ################
# @admin.register(Patologia)
# class PatologiaAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'paciente', 'medico', 'fecha_registro')
#     search_fields = ('nombre', 'paciente__numero_ficha')
#     list_filter = ('fecha_registro',)
#     readonly_fields = ('fecha_registro',)
#
#
# ################
# # Admin: Procedimiento
# # Descripción: Registro de procedimientos en el administrador
# ################
# @admin.register(Procedimiento)
# class ProcedimientoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'paciente', 'realizado_por', 'fecha_procedimiento')
#     search_fields = ('nombre', 'paciente__numero_ficha')
#     list_filter = ('fecha_procedimiento',)
#     readonly_fields = ('fecha_procedimiento',)
#
#
# ################
# # Admin: Medicamento
# # Descripción: Registro de medicamentos en el administrador
# ################
# @admin.register(Medicamento)
# class MedicamentoAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'paciente', 'dosis', 'administrado_por', 'fecha_administracion')
#     search_fields = ('nombre', 'paciente__numero_ficha')
#     list_filter = ('fecha_administracion',)
#     readonly_fields = ('fecha_administracion',)