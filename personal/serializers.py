from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

################
# Serializer: UsuarioSerializer
# Descripción: Serializa el modelo User para la API
################
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]


################
# Serializer: PerfilSerializer
# Descripción: Serializa el modelo Perfil para la API
################
class PerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    usuario_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Perfil
        fields = [
            'id',
            'usuario',
            'usuario_id',
            'rol',
            'numero_colegio',
            'especialidad',
            'activo',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']