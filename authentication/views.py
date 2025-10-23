from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

################
# VISTA: Login
################
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de login personalizada
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, '⚠️ Por favor ingrese usuario y contraseña')
            return render(request, 'authentication/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ ¡Bienvenido {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, '❌ Usuario o contraseña incorrectos')
    
    return render(request, 'authentication/login.html')


################
# VISTA: Logout
################
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.success(request, '✅ Ha cerrado sesión correctamente')
    return redirect('authentication:login')


################
# VISTA: Dashboard (requiere login)
################
@login_required(login_url='authentication:login')
def dashboard(request):
    """
    Dashboard principal diferenciado por rol
    """
    user = request.user
    
    # Obtener el rol del usuario (desde groups de Django o custom field)
    rol = get_user_role(user)
    
    # Determinar qué template mostrar según el rol
    templates_por_rol = {
        'ADMINISTRADOR': 'core/data/dashboard_admin.html',
        'MEDICO': 'core/data/dashboard_medico.html',
        'MATRONA': 'core/data/dashboard_matrona.html',
        'TENS': 'core/data/dashboard_tens.html',
    }
    
    template = templates_por_rol.get(rol, 'core/data/home.html')
    
    context = {
        'user': user,
        'rol': rol,
        'modulos': get_modulos_por_rol(rol),
    }
    
    return render(request, template, context)


################
# FUNCIONES AUXILIARES
################

def get_user_role(user):
    """
    Obtiene el rol del usuario
    Busca en groups de Django (recomendado)
    """
    if user.is_superuser:
        return 'ADMINISTRADOR'
    
    # Si tiene groups de Django
    groups = user.groups.values_list('name', flat=True)
    
    if 'Administrativo' in groups or 'ADMINISTRADOR' in groups:
        return 'ADMINISTRADOR'
    elif 'Medico' in groups or 'MÉDICO' in groups:
        return 'MEDICO'
    elif 'Matrona' in groups or 'MATRONA' in groups:
        return 'MATRONA'
    elif 'TENS' in groups or 'Tens' in groups:
        return 'TENS'
    
    # Por defecto
    return 'USUARIO'


def get_modulos_por_rol(rol):
    """
    Retorna los módulos disponibles según el rol
    """
    modulos_base = {
        'ADMINISTRADOR': [
            {
                'nombre': 'Personas',
                'icono': 'bi-people-fill',
                'url': '/app/core/personas/',
                'color': 'primary',
                'estado': 'Activo',
                'descripcion': 'Gestión de personas en el sistema'
            },
            {
                'nombre': 'Admisiones',
                'icono': 'bi-door-open',
                'url': '#',
                'color': 'success',
                'estado': 'Próximo',
                'descripcion': 'Registro de admisiones hospitalarias'
            },
            {
                'nombre': 'Pacientes',
                'icono': 'bi-person-heart',
                'url': '#',
                'color': 'danger',
                'estado': 'Próximo',
                'descripcion': 'Fichas clínicas de pacientes'
            },
            {
                'nombre': 'Registros',
                'icono': 'bi-file-text',
                'url': '#',
                'color': 'warning',
                'estado': 'Próximo',
                'descripcion': 'Observaciones y procedimientos'
            },
            {
                'nombre': 'Personal',
                'icono': 'bi-person-badge',
                'url': '#',
                'color': 'info',
                'estado': 'Próximo',
                'descripcion': 'Gestión de usuarios y roles'
            },
            {
                'nombre': 'Reportes',
                'icono': 'bi-bar-chart',
                'url': '#',
                'color': 'secondary',
                'estado': 'Próximo',
                'descripcion': 'Reportes y análisis'
            },
        ],
        'MEDICO': [
            {
                'nombre': 'Pacientes',
                'icono': 'bi-person-heart',
                'url': '#',
                'color': 'danger',
                'estado': 'Activo',
                'descripcion': 'Ver fichas de pacientes'
            },
            {
                'nombre': 'Controles',
                'icono': 'bi-calendar-check',
                'url': '#',
                'color': 'info',
                'estado': 'Activo',
                'descripcion': 'Controles prenatales'
            },
            {
                'nombre': 'Observaciones',
                'icono': 'bi-file-text',
                'url': '#',
                'color': 'warning',
                'estado': 'Activo',
                'descripcion': 'Mis observaciones médicas'
            },
            {
                'nombre': 'Reportes',
                'icono': 'bi-bar-chart',
                'url': '#',
                'color': 'secondary',
                'estado': 'Activo',
                'descripcion': 'Mis reportes'
            },
        ],
        'MATRONA': [
            {
                'nombre': 'Pacientes',
                'icono': 'bi-person-heart',
                'url': '#',
                'color': 'danger',
                'estado': 'Activo',
                'descripcion': 'Fichas de pacientes'
            },
            {
                'nombre': 'Controles',
                'icono': 'bi-calendar-check',
                'url': '#',
                'color': 'info',
                'estado': 'Activo',
                'descripcion': 'Crear controles prenatales'
            },
            {
                'nombre': 'Observaciones',
                'icono': 'bi-file-text',
                'url': '#',
                'color': 'warning',
                'estado': 'Activo',
                'descripcion': 'Registrar observaciones'
            },
        ],
        'TENS': [
            {
                'nombre': 'Procedimientos',
                'icono': 'bi-scissors',
                'url': '#',
                'color': 'info',
                'estado': 'Activo',
                'descripcion': 'Registrar procedimientos'
            },
            {
                'nombre': 'Medicamentos',
                'icono': 'bi-capsule',
                'url': '#',
                'color': 'danger',
                'estado': 'Activo',
                'descripcion': 'Administrar medicamentos'
            },
        ],
    }
    
    return modulos_base.get(rol, [])