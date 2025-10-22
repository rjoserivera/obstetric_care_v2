from rest_framework import serializers
from .models import Admision
from core.serializers import PersonaSerializer

################
# Serializer: AdmisionSerializer
# Descripción: Serializa el modelo Admision para la API
################
class AdmisionSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    persona_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Admision
        fields = [
            'id',
            'persona',
            'persona_id',
            'previsión',
            'estado',
            'fecha_admision',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_admision', 'fecha_actualizacion']