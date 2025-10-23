from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ⚠️ TEMPORALMENTE DESHABILITADO - PerfilViewSet no existe aún
# from .views import PerfilViewSet

################
# Router: personal
# Descripción: Rutas de la app personal
################
router = DefaultRouter()
# router.register(r'perfiles', PerfilViewSet, basename='perfil')

urlpatterns = [
    path('', include(router.urls)),
]