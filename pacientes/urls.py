from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacienteViewSet, ControlPrenatalViewSet

################
# Router: pacientes
# Descripción: Rutas de la app pacientes
################
router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'controles', ControlPrenatalViewSet, basename='control-prenatal')

urlpatterns = [
    path('', include(router.urls)),
]