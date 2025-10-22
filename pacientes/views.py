from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Paciente, ControlPrenatal
from .serializers import PacienteSerializer, ControlPrenatalSerializer

################
# ViewSet: PacienteViewSet
# Descripción: API para gestionar Pacientes
################
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['numero_ficha', 'persona__rut', 'persona__nombre']
    ordering_fields = ['fecha_creacion']
    
    ################
    # Acción: historial_completo
    # Descripción: Obtiene el historial completo del paciente
    ################
    @action(detail=True, methods=['get'])
    def historial_completo(self, request, pk=None):
        paciente = self.get_object()
        controles = paciente.controles.all()
        
        data = {
            'paciente': PacienteSerializer(paciente).data,
            'controles': ControlPrenatalSerializer(controles, many=True).data,
        }
        return Response(data)


################
# ViewSet: ControlPrenatalViewSet
# Descripción: API para gestionar Controles Prenatales
################
class ControlPrenatalViewSet(viewsets.ModelViewSet):
    queryset = ControlPrenatal.objects.all()
    serializer_class = ControlPrenatalSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['paciente__numero_ficha']
    ordering_fields = ['fecha_control']
    
    ################
    # Filtrado por paciente
    # Descripción: Filtra controles por ID de paciente
    ################
    def get_queryset(self):
        queryset = super().get_queryset()
        paciente_id = self.request.query_params.get('paciente_id')
        
        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)
        
        return queryset