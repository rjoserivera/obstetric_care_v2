from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ObservacionViewSet,
    PatologiaViewSet,
    ProcedimientoViewSet,
    MedicamentoViewSet
)

################
# Router: registros
# Descripción: Rutas de la app registros
################
router = DefaultRouter()
router.register(r'observaciones', ObservacionViewSet, basename='observacion')
router.register(r'patologias', PatologiaViewSet, basename='patologia')
router.register(r'procedimientos', ProcedimientoViewSet, basename='procedimiento')
router.register(r'medicamentos', MedicamentoViewSet, basename='medicamento')

urlpatterns = [
    path('', include(router.urls)),
]