from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonaViewSet

################
# Router: core
# Descripción: Rutas de la app core
################
router = DefaultRouter()
router.register(r'personas', PersonaViewSet, basename='persona')

urlpatterns = [
    path('', include(router.urls)),
]