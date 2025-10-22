from rest_framework import serializers
from .models import Paciente, ControlPrenatal
from core.serializers import PersonaSerializer

################
# Serializer: PacienteSerializer
# Descripción: Serializa el modelo Paciente para la API
################
class PacienteSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    persona_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Paciente
        fields = [
            'id',
            'persona',
            'persona_id',
            'numero_ficha',
            'embarazos_previos',
            'partos_previos',
            'abortos_previos',
            'hipertension',
            'diabetes',
            'diabetes_gestacional',
            'otras_patologias',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


################
# Serializer: ControlPrenatalSerializer
# Descripción: Serializa el modelo ControlPrenatal para la API
################
class ControlPrenatalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlPrenatal
        fields = [
            'id',
            'paciente',
            'fecha_control',
            'semanas_gestacion',
            'peso',
            'presion',
            'observaciones',
            'fecha_registro',
        ]
        read_only_fields = ['fecha_registro']