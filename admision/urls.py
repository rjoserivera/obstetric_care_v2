from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdmisionViewSet

################
# Router: admision
# Descripción: Rutas de la app admision
################
router = DefaultRouter()
router.register(r'admisiones', AdmisionViewSet, basename='admision')

urlpatterns = [
    path('', include(router.urls)),
]