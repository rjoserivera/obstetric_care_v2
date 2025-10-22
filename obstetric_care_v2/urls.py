from django.contrib import admin
from django.urls import path, include

################
# URLs principales
# Descripción: Rutas principales del proyecto
################
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/core/', include('core.urls')),
    path('api/admision/', include('admision.urls')),
    path('api/pacientes/', include('pacientes.urls')),
    path('api/registros/', include('registros.urls')),
    path('api/personal/', include('personal.urls')),
    
    # DRF Auth
    path('api-auth/', include('rest_framework.urls')),
]