from django.contrib import admin

# ⚠️ TEMPORALMENTE DESHABILITADO - Modelo Perfil no existe aún
# from .models import Perfil
#
# ################
# # Admin: Perfil
# # Descripción: Registro de perfiles de usuario en el administrador
# ################
# @admin.register(Perfil)
# class PerfilAdmin(admin.ModelAdmin):
#     list_display = ('usuario', 'rol', 'numero_colegio', 'activo', 'fecha_creacion')
#     search_fields = ('usuario__username', 'usuario__first_name', 'numero_colegio')
#     list_filter = ('rol', 'activo', 'fecha_creacion')
#     readonly_fields = ('fecha_creacion', 'fecha_actualizacion')