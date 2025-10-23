from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Persona

@login_required(login_url='authentication:login')
def personas_list(request):
    # Solo mostrar personas activas
    personas = Persona.objects.filter(Activo=True).order_by('-fecha_creacion')
    
    query = request.GET.get('q')
    if query:
        personas = personas.filter(
            Nombre__icontains=query
        ) | personas.filter(
            Apellido_Paterno__icontains=query
        ) | personas.filter(
            Rut__icontains=query
        ) | personas.filter(
            Email__icontains=query
        )
    
    context = {
        'personas': personas,
        'query': query,
    }
    
    return render(request, 'core/data/personas_list.html', context)


@login_required(login_url='authentication:login')
def personas_create(request):
    if request.method == 'POST':
        try:
            rut = request.POST.get('rut', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido_paterno = request.POST.get('apellido_paterno', '').strip()
            apellido_materno = request.POST.get('apellido_materno', '').strip()
            fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
            genero = request.POST.get('genero', '').strip()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            comuna = request.POST.get('ciudad', '').strip()
            
            errores = []
            
            if not rut:
                errores.append('RUT es requerido')
            if not nombre:
                errores.append('Nombre es requerido')
            if not apellido_paterno:
                errores.append('Apellido Paterno es requerido')
            if not apellido_materno:
                errores.append('Apellido Materno es requerido')
            if not fecha_nacimiento:
                errores.append('Fecha de Nacimiento es requerida')
            if not genero:
                errores.append('Género es requerido')
            if not telefono:
                errores.append('Teléfono es requerido')
            if not direccion:
                errores.append('Dirección es requerida')
            if not comuna:
                errores.append('Comuna es requerida')
            
            if errores:
                for error in errores:
                    messages.error(request, f'❌ {error}')
            else:
                persona = Persona.objects.create(
                    Rut=rut,
                    Nombre=nombre,
                    Apellido_Paterno=apellido_paterno,
                    Apellido_Materno=apellido_materno,
                    Fecha_nacimiento=fecha_nacimiento,
                    Sexo=genero,
                    Email=email if email else '',
                    Telefono=telefono,
                    Direccion=direccion,
                    Comuna=comuna,
                    Activo=True
                )
                
                messages.success(
                    request,
                    f'✅ Persona registrada exitosamente: {persona.Nombre} {persona.Apellido_Paterno}'
                )
                return redirect('core:personas_list')
                
        except IntegrityError as e:
            if 'Rut' in str(e) or 'rut' in str(e).lower():
                messages.error(request, '❌ Este RUT ya está registrado en el sistema')
            else:
                messages.error(request, f'❌ Error de integridad: {str(e)}')
        except ValueError as e:
            messages.error(request, f'❌ Error en los datos: {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Error al guardar la persona: {str(e)}')
    
    return render(request, 'core/formularios/persona_form.html')


@login_required(login_url='authentication:login')
def personas_edit(request, pk):
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if request.method == 'POST':
        try:
            rut = request.POST.get('rut', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido_paterno = request.POST.get('apellido_paterno', '').strip()
            apellido_materno = request.POST.get('apellido_materno', '').strip()
            fecha_nacimiento = request.POST.get('fecha_nacimiento', '').strip()
            genero = request.POST.get('genero', '').strip()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            comuna = request.POST.get('ciudad', '').strip()
            
            errores = []
            
            if not rut:
                errores.append('RUT es requerido')
            if not nombre:
                errores.append('Nombre es requerido')
            if not apellido_paterno:
                errores.append('Apellido Paterno es requerido')
            if not apellido_materno:
                errores.append('Apellido Materno es requerido')
            if not fecha_nacimiento:
                errores.append('Fecha de Nacimiento es requerida')
            if not genero:
                errores.append('Género es requerido')
            if not telefono:
                errores.append('Teléfono es requerido')
            if not direccion:
                errores.append('Dirección es requerida')
            if not comuna:
                errores.append('Comuna es requerida')
            
            if errores:
                for error in errores:
                    messages.error(request, f'❌ {error}')
            else:
                persona.Rut = rut
                persona.Nombre = nombre
                persona.Apellido_Paterno = apellido_paterno
                persona.Apellido_Materno = apellido_materno
                persona.Fecha_nacimiento = fecha_nacimiento
                persona.Sexo = genero
                persona.Email = email if email else ''
                persona.Telefono = telefono
                persona.Direccion = direccion
                persona.Comuna = comuna
                persona.save()
                
                messages.success(
                    request,
                    f'✅ Persona actualizada: {persona.Nombre} {persona.Apellido_Paterno}'
                )
                return redirect('core:personas_list')
                
        except IntegrityError as e:
            messages.error(request, '❌ Este RUT ya está registrado en el sistema')
        except ValueError as e:
            messages.error(request, f'❌ Error en los datos: {str(e)}')
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar: {str(e)}')
    
    context = {'persona': persona}
    return render(request, 'core/formularios/persona_form.html', context)


@login_required(login_url='authentication:login')
def personas_detail(request, pk):
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    return render(request, 'core/data/persona_detail.html', {'persona': persona})


@login_required(login_url='authentication:login')
def personas_delete(request, pk):
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if request.method == 'POST':
        nombre = f"{persona.Nombre} {persona.Apellido_Paterno}"
        # Soft delete: marcar como inactivo
        persona.Activo = False
        persona.save()
        messages.success(request, f'✅ Persona desactivada: {nombre}')
        return redirect('core:personas_list')
    
    return render(request, 'core/data/persona_confirm_delete.html', {'persona': persona})