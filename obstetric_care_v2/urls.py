from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('authentication:login')

urlpatterns = [
    path('', redirect_to_login),  # ← Redirige raíz a login
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('home/', TemplateView.as_view(template_name='core/data/home.html'), name='home'),
    path('app/core/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
]