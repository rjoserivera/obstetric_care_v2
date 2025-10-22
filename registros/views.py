from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Observacion, Patologia, Procedimiento, Medicamento
from .serializers import (
    ObservacionSerializer,
    PatologiaSerializer,
    ProcedimientoSerializer,
    MedicamentoSerializer
)

################
# ViewSet: ObservacionViewSet
# Descripción: API para gestionar Observaciones médicas
################
class ObservacionViewSet(viewsets.ModelViewSet):
    queryset = Observacion.objects.all()
    serializer_class = ObservacionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['paciente__numero_ficha']
    ordering_fields = ['fecha_creacion']


################
# ViewSet: PatologiaViewSet
# Descripción: API para gestionar Patologías
################
class PatologiaViewSet(viewsets.ModelViewSet):
    queryset = Patologia.objects.all()
    serializer_class = PatologiaSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'paciente__numero_ficha']
    ordering_fields = ['fecha_registro']


################
# ViewSet: ProcedimientoViewSet
# Descripción: API para gestionar Procedimientos
################
class ProcedimientoViewSet(viewsets.ModelViewSet):
    queryset = Procedimiento.objects.all()
    serializer_class = ProcedimientoSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'paciente__numero_ficha']
    ordering_fields = ['fecha_procedimiento']


################
# ViewSet: MedicamentoViewSet
# Descripción: API para gestionar Medicamentos
################
class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'paciente__numero_ficha']
    ordering_fields = ['fecha_administracion']