from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Admision
from .serializers import AdmisionSerializer
from core.models import Persona
from core.serializers import PersonaSerializer

################
# ViewSet: AdmisionViewSet
# Descripción: API para gestionar Admisiones
################
class AdmisionViewSet(viewsets.ModelViewSet):
    queryset = Admision.objects.all()
    serializer_class = AdmisionSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['persona__rut', 'persona__nombre']
    ordering_fields = ['fecha_admision']
    
    ################
    # Acción: crear_persona_admision
    # Descripción: Crea una Persona e Admision en un solo paso
    ################
    @action(detail=False, methods=['post'])
    def crear_persona_admision(self, request):
        # Crear Persona
        persona_data = {
            'rut': request.data.get('rut'),
            'nombre': request.data.get('nombre'),
            'apellido': request.data.get('apellido'),
            'edad': request.data.get('edad'),
            'direccion': request.data.get('direccion'),
            'telefono': request.data.get('telefono'),
            'email': request.data.get('email'),
        }
        
        persona_serializer = PersonaSerializer(data=persona_data)
        if not persona_serializer.is_valid():
            return Response(
                persona_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        persona = persona_serializer.save()
        
        # Crear Admision
        admision_data = {
            'persona': persona.id,
            'previsión': request.data.get('previsión'),
            'estado': 'activo',
        }
        
        admision_serializer = AdmisionSerializer(data=admision_data)
        if not admision_serializer.is_valid():
            persona.delete()
            return Response(
                admision_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        admision_serializer.save()
        return Response(admision_serializer.data, status=status.HTTP_201_CREATED)