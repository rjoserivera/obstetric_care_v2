from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# ⚠️ TEMPORALMENTE DESHABILITADO - Modelo Perfil no existe aún
# from .models import Perfil
# from .serializers import PerfilSerializer, UsuarioSerializer

################
# ViewSet: PerfilViewSet
# Descripción: API para gestionar Perfiles de usuarios
# ESTADO: Deshabilitado temporalmente
################
# class PerfilViewSet(viewsets.ModelViewSet):
#     queryset = Perfil.objects.all()
#     serializer_class = PerfilSerializer
#     permission_classes = [IsAuthenticated]
#     search_fields = ['usuario__username', 'rol']
#     ordering_fields = ['fecha_creacion']
#     
#     ################
#     # Acción: por_rol
#     # Descripción: Obtiene perfiles filtrados por rol
#     ################
#     @action(detail=False, methods=['get'])
#     def por_rol(self, request):
#         rol = request.query_params.get('rol')
#         
#         if not rol:
#             return Response(
#                 {'error': 'El parámetro rol es requerido'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         
#         perfiles = Perfil.objects.filter(rol=rol, activo=True)
#         serializer = self.get_serializer(perfiles, many=True)
#         return Response(serializer.data)
#     
#     ################
#     # Acción: mi_perfil
#     # Descripción: Obtiene el perfil del usuario autenticado
#     ################
#     @action(detail=False, methods=['get'])
#     def mi_perfil(self, request):
#         try:
#             perfil = Perfil.objects.get(usuario=request.user)
#             serializer = self.get_serializer(perfil)
#             return Response(serializer.data)
#         except Perfil.DoesNotExist:
#             return Response(
#                 {'error': 'No tiene perfil asignado'},
#                 status=status.HTTP_404_NOT_FOUND
#             )