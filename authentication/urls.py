from django.urls import path
from .views import login_view, logout_view, dashboard

app_name = 'authentication'  # ← Asegúrate de que sea 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]