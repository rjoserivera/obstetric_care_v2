from django.urls import path
from .views import (
    personas_list,
    personas_create,
    personas_edit,
    personas_detail,
    personas_delete,
)

app_name = 'core'

urlpatterns = [
    path('personas/', personas_list, name='personas_list'),
    path('personas/crear/', personas_create, name='personas_create'),
    path('personas/<int:pk>/editar/', personas_edit, name='personas_edit'),
    path('personas/<int:pk>/ver/', personas_detail, name='personas_detail'),
    path('personas/<int:pk>/eliminar/', personas_delete, name='personas_delete'),
]