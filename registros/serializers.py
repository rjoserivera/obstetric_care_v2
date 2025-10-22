from rest_framework import serializers
from .models import Observacion, Patologia, Procedimiento, Medicamento

################
# Serializer: ObservacionSerializer
# Descripción: Serializa el modelo Observacion para la API
################
class ObservacionSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.CharField(source='medico.get_full_name', read_only=True)
    
    class Meta:
        model = Observacion
        fields = [
            'id',
            'paciente',
            'medico',
            'medico_nombre',
            'texto',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


################
# Serializer: PatologiaSerializer
# Descripción: Serializa el modelo Patologia para la API
################
class PatologiaSerializer(serializers.ModelSerializer):
    medico_nombre = serializers.CharField(source='medico.get_full_name', read_only=True)
    
    class Meta:
        model = Patologia
        fields = [
            'id',
            'paciente',
            'nombre',
            'descripcion',
            'medico',
            'medico_nombre',
            'fecha_registro',
        ]
        read_only_fields = ['fecha_registro']


################
# Serializer: ProcedimientoSerializer
# Descripción: Serializa el modelo Procedimiento para la API
################
class ProcedimientoSerializer(serializers.ModelSerializer):
    realizado_por_nombre = serializers.CharField(source='realizado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Procedimiento
        fields = [
            'id',
            'paciente',
            'nombre',
            'descripcion',
            'realizado_por',
            'realizado_por_nombre',
            'fecha_procedimiento',
        ]
        read_only_fields = ['fecha_procedimiento']


################
# Serializer: MedicamentoSerializer
# Descripción: Serializa el modelo Medicamento para la API
################
class MedicamentoSerializer(serializers.ModelSerializer):
    administrado_por_nombre = serializers.CharField(source='administrado_por.get_full_name', read_only=True)
    
    class Meta:
        model = Medicamento
        fields = [
            'id',
            'paciente',
            'nombre',
            'dosis',
            'via_administracion',
            'administrado_por',
            'administrado_por_nombre',
            'fecha_administracion',
        ]
        read_only_fields = ['fecha_administracion']