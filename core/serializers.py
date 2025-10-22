from rest_framework import serializers
from .models import Persona

################
# Serializer: PersonaSerializer
# Descripción: Serializa el modelo Persona para la API
################
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            'id',
            'rut',
            'nombre',
            'apellido',
            'edad',
            'direccion',
            'telefono',
            'email',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']