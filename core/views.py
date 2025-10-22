from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Persona
from .serializers import PersonaSerializer

################
# ViewSet: PersonaViewSet
# Descripción: API para gestionar Personas
################
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['rut', 'nombre', 'apellido']
    ordering_fields = ['fecha_creacion']
    
    ################
    # Acción: buscar_por_rut
    # Descripción: Busca una persona por RUT
    ################
    @action(detail=False, methods=['get'])
    def buscar_por_rut(self, request):
        rut = request.query_params.get('rut', None)
        if rut is None:
            return Response(
                {'error': 'El parámetro rut es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            persona = Persona.objects.get(rut=rut)
            serializer = self.get_serializer(persona)
            return Response(serializer.data)
        except Persona.DoesNotExist:
            return Response(
                {'error': 'Persona no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )