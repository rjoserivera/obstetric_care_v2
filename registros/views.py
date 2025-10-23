################
# VISTAS: Registros - Observación, Patología, Procedimiento y Medicamento
# Descripción: Vistas para registros clínicos
# v0.2: Con decoradores de permiso y auditoría
################

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

# ====================================================================
# IMPORTANTE: Importar formularios desde las carpetas individuales
# Descomenta según necesites
# ====================================================================

# from registros.Forms.Form_agregar_observacion import Form_agregar_observacion
# from registros.Forms.Form_editar_observacion import Form_editar_observacion
# from registros.Forms.Form_agregar_patologia import Form_agregar_patologia
# from registros.Forms.Form_editar_patologia import Form_editar_patologia
# from registros.Forms.Form_registrar_procedimiento import Form_registrar_procedimiento
# from registros.Forms.Form_editar_procedimiento import Form_editar_procedimiento
# from registros.Forms.Form_prescribir_medicamento import Form_prescribir_medicamento
# from registros.Forms.Form_administrar_medicamento import Form_administrar_medicamento
# from registros.Forms.Form_editar_medicamento import Form_editar_medicamento

from registros.models import Observacion, Patologia, Procedimiento, Medicamento
from pacientes.models import Paciente


# ====================================================================
# UTILIDAD: Mixin para validar permisos por rol
# ====================================================================

class RolRequiredMixin(UserPassesTestMixin):
    """Mixin para validar rol del usuario."""
    roles_permitidos = []
    
    def test_func(self):
        if not hasattr(self.request.user, 'profile'):
            return False
        return self.request.user.profile.rol in self.roles_permitidos
    
    def handle_no_permission(self):
        messages.error(self.request, 'No tiene permiso para esta acción.')
        return redirect('dashboard')


# ====================================================================
# OBSERVACIÓN
# ====================================================================

class AgregarObservacionView(LoginRequiredMixin, RolRequiredMixin, CreateView):
    """
    Vista para agregar una observación clínica.
    Permite anexar imagen.
    Usado por: Matrona, Médico
    """
    model = Observacion
    # form_class = Form_agregar_observacion  # Descomenta cuando crees el archivo
    template_name = 'registros/observaciones/agregar_observacion.html'
    fields = ['texto', 'imagen']
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Crea la observación."""
        paciente_id = self.kwargs.get('paciente_id')
        form.instance.paciente_id = paciente_id
        form.instance.created_by = self.request.user
        
        messages.success(self.request, 'Observación registrada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': self.kwargs.get('paciente_id')}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Nueva Observación - {context['paciente'].persona.get_full_name()}"
        return context


class EditarObservacionView(LoginRequiredMixin, RolRequiredMixin, UpdateView):
    """
    Vista para editar una observación.
    Usado por: Matrona, Médico
    """
    model = Observacion
    # form_class = Form_editar_observacion  # Descomenta cuando crees el archivo
    template_name = 'registros/observaciones/editar_observacion.html'
    fields = ['texto', 'imagen']
    pk_url_kwarg = 'pk'
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Actualiza la observación."""
        form.instance.modified_by = self.request.user
        messages.success(self.request, 'Observación actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        obs = self.get_object()
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': obs.paciente.pk}
        )


# ====================================================================
# PATOLOGÍA
# ====================================================================

class AgregarPatologiaView(LoginRequiredMixin, RolRequiredMixin, CreateView):
    """
    Vista para diagnosticar una patología.
    Permite anexar imagen de diagnóstico.
    Usado por: Matrona, Médico
    """
    model = Patologia
    # form_class = Form_agregar_patologia  # Descomenta cuando crees el archivo
    template_name = 'registros/patologias/agregar_patologia.html'
    fields = ['nombre', 'codigo_cie_10', 'descripcion', 'imagen', 
              'nivel_riesgo', 'protocolo_seguimiento', 'fecha_diagnostico']
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Crea la patología."""
        paciente_id = self.kwargs.get('paciente_id')
        form.instance.paciente_id = paciente_id
        form.instance.created_by = self.request.user
        form.instance.diagnosticado_por = self.request.user
        form.instance.estado = 'activa'
        
        messages.success(
            self.request,
            f'Patología {form.instance.nombre} diagnosticada para el paciente.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': self.kwargs.get('paciente_id')}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Nuevo Diagnóstico - {context['paciente'].persona.get_full_name()}"
        return context


class EditarPatologiaView(LoginRequiredMixin, RolRequiredMixin, UpdateView):
    """
    Vista para editar una patología.
    Permite cambiar estado (activa/resuelta/inactiva).
    Usado por: Matrona, Médico
    """
    model = Patologia
    # form_class = Form_editar_patologia  # Descomenta cuando crees el archivo
    template_name = 'registros/patologias/editar_patologia.html'
    fields = ['nombre', 'codigo_cie_10', 'descripcion', 'imagen', 
              'nivel_riesgo', 'protocolo_seguimiento', 'estado', 'fecha_resolucion']
    pk_url_kwarg = 'pk'
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Actualiza la patología."""
        form.instance.modified_by = self.request.user
        
        # Si cambia a resuelta, asignar fecha de resolución
        if form.instance.estado == 'resuelta' and not form.instance.fecha_resolucion:
            form.instance.fecha_resolucion = timezone.now().date()
        
        messages.success(self.request, 'Patología actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        patologia = self.get_object()
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': patologia.paciente.pk}
        )


class ListarPatologiasView(LoginRequiredMixin, RolRequiredMixin, ListView):
    """
    Vista para listar patologías de un paciente.
    Usado por: Administrativo, Matrona, Médico
    """
    model = Patologia
    template_name = 'registros/patologias/listar_patologias.html'
    context_object_name = 'patologias'
    paginate_by = 20
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def get_queryset(self):
        """Retorna patologías del paciente."""
        paciente_id = self.kwargs.get('paciente_id')
        return Patologia.objects.filter(
            paciente_id=paciente_id
        ).order_by('-fecha_diagnostico')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Patologías - {context['paciente'].persona.get_full_name()}"
        return context


# ====================================================================
# PROCEDIMIENTO
# ====================================================================

class RegistrarProcedimientoView(LoginRequiredMixin, RolRequiredMixin, CreateView):
    """
    Vista para registrar un procedimiento.
    Permite anexar foto de evidencia.
    Usado por: Matrona, Médico, TENS
    """
    model = Procedimiento
    # form_class = Form_registrar_procedimiento  # Descomenta cuando crees el archivo
    template_name = 'registros/procedimientos/registrar_procedimiento.html'
    fields = ['tipo_procedimiento', 'descripcion', 'fecha_procedimiento', 
              'material_utilizado', 'imagen', 'observaciones']
    roles_permitidos = ['administrativo', 'matrona', 'medico', 'tens']
    
    def form_valid(self, form):
        """Crea el procedimiento."""
        paciente_id = self.kwargs.get('paciente_id')
        form.instance.paciente_id = paciente_id
        form.instance.created_by = self.request.user
        form.instance.realizado_por = self.request.user
        form.instance.estado = 'realizado'
        
        messages.success(
            self.request,
            f'Procedimiento {form.instance.get_tipo_procedimiento_display()} registrado exitosamente.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': self.kwargs.get('paciente_id')}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Registrar Procedimiento - {context['paciente'].persona.get_full_name()}"
        return context


class EditarProcedimientoView(LoginRequiredMixin, RolRequiredMixin, UpdateView):
    """
    Vista para editar un procedimiento.
    Usado por: Matrona, Médico, TENS
    """
    model = Procedimiento
    # form_class = Form_editar_procedimiento  # Descomenta cuando crees el archivo
    template_name = 'registros/procedimientos/editar_procedimiento.html'
    fields = ['tipo_procedimiento', 'descripcion', 'fecha_procedimiento', 
              'material_utilizado', 'imagen', 'estado', 'observaciones']
    pk_url_kwarg = 'pk'
    roles_permitidos = ['administrativo', 'matrona', 'medico', 'tens']
    
    def form_valid(self, form):
        """Actualiza el procedimiento."""
        form.instance.modified_by = self.request.user
        messages.success(self.request, 'Procedimiento actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        proc = self.get_object()
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': proc.paciente.pk}
        )


class ListarProcedimientosView(LoginRequiredMixin, RolRequiredMixin, ListView):
    """
    Vista para listar procedimientos de un paciente.
    Usado por: Administrativo, Matrona, Médico, TENS
    """
    model = Procedimiento
    template_name = 'registros/procedimientos/listar_procedimientos.html'
    context_object_name = 'procedimientos'
    paginate_by = 20
    roles_permitidos = ['administrativo', 'matrona', 'medico', 'tens']
    
    def get_queryset(self):
        """Retorna procedimientos del paciente."""
        paciente_id = self.kwargs.get('paciente_id')
        return Procedimiento.objects.filter(
            paciente_id=paciente_id
        ).order_by('-fecha_procedimiento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Procedimientos - {context['paciente'].persona.get_full_name()}"
        return context


# ====================================================================
# MEDICAMENTO
# ====================================================================

class PrescrbirMedicamentoView(LoginRequiredMixin, RolRequiredMixin, CreateView):
    """
    Vista para prescribir un medicamento.
    Usado por: Médico, Matrona
    """
    model = Medicamento
    # form_class = Form_prescribir_medicamento  # Descomenta cuando crees el archivo
    template_name = 'registros/medicamentos/prescribir_medicamento.html'
    fields = ['nombre_medicamento', 'dosis', 'via_administracion', 
              'frecuencia', 'duracion_dias', 'indicacion', 'fecha_prescripcion']
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Crea la prescripción."""
        paciente_id = self.kwargs.get('paciente_id')
        form.instance.paciente_id = paciente_id
        form.instance.created_by = self.request.user
        form.instance.prescrito_por = self.request.user
        form.instance.estado = 'prescrito'
        
        messages.success(
            self.request,
            f'Medicamento {form.instance.nombre_medicamento} prescrito exitosamente.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': self.kwargs.get('paciente_id')}
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Prescribir Medicamento - {context['paciente'].persona.get_full_name()}"
        return context


class AdministrarMedicamentoView(LoginRequiredMixin, RolRequiredMixin, UpdateView):
    """
    Vista para registrar la administración de un medicamento.
    Usado por: TENS, Matrona, Médico
    """
    model = Medicamento
    # form_class = Form_administrar_medicamento  # Descomenta cuando crees el archivo
    template_name = 'registros/medicamentos/administrar_medicamento.html'
    fields = ['estado', 'fecha_administracion', 'observaciones']
    pk_url_kwarg = 'pk'
    roles_permitidos = ['administrativo', 'matrona', 'medico', 'tens']
    
    def get_queryset(self):
        """Solo medicamentos prescritos."""
        return Medicamento.objects.filter(estado='prescrito')
    
    def form_valid(self, form):
        """Registra la administración."""
        form.instance.modified_by = self.request.user
        form.instance.administrado_por = self.request.user
        form.instance.estado = 'administrado'
        
        messages.success(
            self.request,
            f'Medicamento {form.instance.nombre_medicamento} registrado como administrado.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        med = self.get_object()
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': med.paciente.pk}
        )


class EditarMedicamentoView(LoginRequiredMixin, RolRequiredMixin, UpdateView):
    """
    Vista para editar un medicamento.
    Usado por: Médico, Matrona
    """
    model = Medicamento
    # form_class = Form_editar_medicamento  # Descomenta cuando crees el archivo
    template_name = 'registros/medicamentos/editar_medicamento.html'
    fields = ['nombre_medicamento', 'dosis', 'via_administracion', 
              'frecuencia', 'duracion_dias', 'indicacion', 'estado', 'observaciones']
    pk_url_kwarg = 'pk'
    roles_permitidos = ['administrativo', 'matrona', 'medico']
    
    def form_valid(self, form):
        """Actualiza el medicamento."""
        form.instance.modified_by = self.request.user
        messages.success(self.request, 'Medicamento actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        med = self.get_object()
        return reverse_lazy(
            'pacientes:detalle_paciente',
            kwargs={'pk': med.paciente.pk}
        )


class ListarMedicamentosView(LoginRequiredMixin, RolRequiredMixin, ListView):
    """
    Vista para listar medicamentos de un paciente.
    Usado por: Administrativo, Matrona, Médico, TENS
    """
    model = Medicamento
    template_name = 'registros/medicamentos/listar_medicamentos.html'
    context_object_name = 'medicamentos'
    paginate_by = 20
    roles_permitidos = ['administrativo', 'matrona', 'medico', 'tens']
    
    def get_queryset(self):
        """Retorna medicamentos del paciente."""
        paciente_id = self.kwargs.get('paciente_id')
        
        # Filtrar por estado si se especifica
        estado = self.request.GET.get('estado')
        queryset = Medicamento.objects.filter(paciente_id=paciente_id)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset.order_by('-fecha_prescripcion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_id = self.kwargs.get('paciente_id')
        context['paciente'] = get_object_or_404(Paciente, pk=paciente_id)
        context['titulo'] = f"Medicamentos - {context['paciente'].persona.get_full_name()}"
        context['estado_choices'] = Medicamento._meta.get_field('estado').choices
        return context


# ====================================================================
# DASHBOARD DE REGISTROS
# ====================================================================

class DashboardRegistrosView(LoginRequiredMixin, RolRequiredMixin):
    """
    Vista para ver resumen de registros pendientes.
    Usado por: Matrona, Médico, TENS
    """
    roles_permitidos = ['matrona', 'medico', 'tens']
    template_name = 'registros/dashboard_registros.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        
        # Medicamentos pendientes de administrar
        context['medicamentos_pendientes'] = Medicamento.objects.filter(
            estado='prescrito'
        ).count()
        
        # Procedimientos registrados hoy
        from django.utils import timezone
        hoy = timezone.now().date()
        context['procedimientos_hoy'] = Procedimiento.objects.filter(
            fecha_procedimiento__date=hoy
        ).count()
        
        # Patologías activas sin resolver
        context['patologias_activas'] = Patologia.objects.filter(
            estado='activa'
        ).count()
        
        return context