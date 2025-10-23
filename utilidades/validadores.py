################
# UTILIDADES: Validadores
# Descripción: Funciones de validación sincronizadas con validadores JavaScript
# v0.2: RUT chileno, edad, teléfono
################

from django.core.exceptions import ValidationError
import re


# ====================================================================
# VALIDADOR RUT CHILENO
# ====================================================================
# Sincronizado con: static/js/validador_rut.js

def validar_rut_chileno(rut):
    """
    Valida un RUT chileno con formato XX.XXX.XXX-K o XXXXXXXX-K.
    
    Args:
        rut (str): RUT a validar (con o sin formato)
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
        
    Ejemplos:
        >>> validar_rut_chileno('12.345.678-5')
        (True, 'RUT válido')
        
        >>> validar_rut_chileno('12.345.678-9')
        (False, 'Dígito verificador incorrecto')
    """
    
    # Limpiar RUT: remover puntos y guiones, convertir a mayúsculas
    rut_limpio = rut.replace('.', '').replace('-', '').upper()
    
    # Validar formato básico: 7-8 dígitos + K o dígito
    if not re.match(r'^\d{7,8}[0-9K]$', rut_limpio):
        return False, 'Formato de RUT inválido. Use: XX.XXX.XXX-K'
    
    # Extraer número y verificador
    numero = int(rut_limpio[:-1])
    verificador = rut_limpio[-1]
    
    # Calcular dígito verificador
    multiplicadores = [2, 3, 4, 5, 6, 7]
    suma = 0
    indice = 0
    
    # Procesar dígitos de derecha a izquierda
    numero_str = str(numero)
    for i in range(len(numero_str) - 1, -1, -1):
        suma += int(numero_str[i]) * multiplicadores[indice % 6]
        indice += 1
    
    # Calcular resto
    resto = 11 - (suma % 11)
    
    # Determinar dígito verificador esperado
    if resto == 11:
        digito_esperado = '0'
    elif resto == 10:
        digito_esperado = 'K'
    else:
        digito_esperado = str(resto)
    
    # Comparar
    if verificador != digito_esperado:
        return False, 'Dígito verificador incorrecto'
    
    return True, 'RUT válido'


def formatear_rut(rut):
    """
    Formatea un RUT a XX.XXX.XXX-K.
    
    Args:
        rut (str): RUT a formatear (con o sin formato)
    
    Returns:
        str: RUT formateado o None si es inválido
        
    Ejemplos:
        >>> formatear_rut('123456785')
        '12.345.678-5'
        
        >>> formatear_rut('12.345.678-5')
        '12.345.678-5'
    """
    
    # Limpiar
    rut_limpio = rut.replace('.', '').replace('-', '').upper()
    
    # Validar longitud
    if len(rut_limpio) < 8:
        return None
    
    # Rellenar con ceros a la izquierda
    numero = rut_limpio[:-1].zfill(8)
    verificador = rut_limpio[-1]
    
    # Formatear: XX.XXX.XXX-K
    return f'{numero[:2]}.{numero[2:5]}.{numero[5:8]}-{verificador}'


def normalizar_rut(rut):
    """
    Normaliza un RUT quitando puntos y guiones.
    
    Args:
        rut (str): RUT a normalizar
    
    Returns:
        str: RUT normalizado (sin puntos ni guiones)
    """
    return rut.replace('.', '').replace('-', '').upper()


# ====================================================================
# VALIDADOR EDAD
# ====================================================================

def validar_edad(edad):
    """
    Valida que la edad esté en rango permitido (12-60 años).
    
    Args:
        edad (int): Edad a validar
    
    Returns:
        tuple: (es_valida: bool, mensaje: str)
        
    Ejemplos:
        >>> validar_edad(25)
        (True, 'Edad válida')
        
        >>> validar_edad(10)
        (False, 'La edad debe estar entre 12 y 60 años')
    """
    
    try:
        edad = int(edad)
    except (ValueError, TypeError):
        return False, 'La edad debe ser un número'
    
    if edad < 12:
        return False, 'La edad mínima es 12 años'
    
    if edad > 60:
        return False, 'La edad máxima es 60 años'
    
    return True, 'Edad válida'


# ====================================================================
# VALIDADOR TELÉFONO
# ====================================================================

def validar_telefono(telefono):
    """
    Valida un teléfono chileno.
    Formatos aceptados:
    - +56912345678 (con código país)
    - +56 9 1234 5678 (con espacios)
    - 912345678 (sin código país)
    - 9 1234 5678 (sin código país, con espacios)
    
    Args:
        telefono (str): Teléfono a validar
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
        
    Ejemplos:
        >>> validar_telefono('+56912345678')
        (True, 'Teléfono válido')
        
        >>> validar_telefono('912345678')
        (True, 'Teléfono válido')
        
        >>> validar_telefono('12345')
        (False, 'Formato de teléfono inválido')
    """
    
    # Limpiar: remover espacios
    telefono_limpio = telefono.replace(' ', '')
    
    # Patrón 1: +56912345678 (con código +56)
    if re.match(r'^\+56[9]\d{8}$', telefono_limpio):
        return True, 'Teléfono válido'
    
    # Patrón 2: 912345678 (9 dígitos, comienza con 9)
    if re.match(r'^9\d{8}$', telefono_limpio):
        return True, 'Teléfono válido'
    
    # Si no coincide con ningún patrón
    return False, 'Formato de teléfono inválido. Use: +56912345678 o 912345678'


def normalizar_telefono(telefono):
    """
    Normaliza un teléfono a formato +56XXXXXXXXX.
    
    Args:
        telefono (str): Teléfono a normalizar
    
    Returns:
        str: Teléfono normalizado o None si es inválido
    """
    
    # Validar primero
    es_valido, _ = validar_telefono(telefono)
    if not es_valido:
        return None
    
    # Limpiar
    telefono_limpio = telefono.replace(' ', '').replace('-', '')
    
    # Si ya tiene +56, retornar como está
    if telefono_limpio.startswith('+56'):
        return telefono_limpio
    
    # Si comienza con 9, agregar +56
    if telefono_limpio.startswith('9'):
        return f'+56{telefono_limpio}'
    
    return None


# ====================================================================
# VALIDADOR DE EMAIL
# ====================================================================

def validar_email(email):
    """
    Valida formato de email básico.
    
    Args:
        email (str): Email a validar
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(patron, email):
        return True, 'Email válido'
    else:
        return False, 'Email inválido'


# ====================================================================
# VALIDADOR DE PRESIÓN ARTERIAL
# ====================================================================

def validar_presion(sistolica, diastolica):
    """
    Valida presión arterial.
    Reglas:
    - Sistólica: 60-220 mmHg
    - Diastólica: 40-140 mmHg
    - Diastólica < Sistólica
    
    Args:
        sistolica (int): Presión sistólica
        diastolica (int): Presión diastólica
    
    Returns:
        tuple: (es_valida: bool, mensaje: str)
    """
    
    try:
        sistolica = int(sistolica)
        diastolica = int(diastolica)
    except (ValueError, TypeError):
        return False, 'La presión debe ser números'
    
    if sistolica < 60 or sistolica > 220:
        return False, 'Presión sistólica debe estar entre 60-220 mmHg'
    
    if diastolica < 40 or diastolica > 140:
        return False, 'Presión diastólica debe estar entre 40-140 mmHg'
    
    if diastolica >= sistolica:
        return False, 'Presión diastólica debe ser menor que sistólica'
    
    return True, 'Presión válida'


# ====================================================================
# VALIDADOR DE GLUCEMIA
# ====================================================================

def validar_glucemia(glucemia):
    """
    Valida nivel de glucemia.
    Rango normal: 70-150 mg/dL (advertencia si está fuera)
    
    Args:
        glucemia (float): Nivel de glucemia en mg/dL
    
    Returns:
        tuple: (es_valida: bool, mensaje: str, advertencia: bool)
    """
    
    try:
        glucemia = float(glucemia)
    except (ValueError, TypeError):
        return False, 'La glucemia debe ser un número', False
    
    if glucemia < 0 or glucemia > 500:
        return False, 'Glucemia fuera de rango (0-500 mg/dL)', False
    
    if glucemia < 70 or glucemia > 150:
        return True, 'Glucemia dentro de rango válido', True  # Advertencia
    
    return True, 'Glucemia normal', False


# ====================================================================
# VALIDADOR DE PESO
# ====================================================================

def validar_peso(peso):
    """
    Valida peso en kg.
    Rango: 30-200 kg
    
    Args:
        peso (float): Peso en kg
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    
    try:
        peso = float(peso)
    except (ValueError, TypeError):
        return False, 'El peso debe ser un número'
    
    if peso < 30 or peso > 200:
        return False, 'Peso debe estar entre 30-200 kg'
    
    return True, 'Peso válido'


# ====================================================================
# VALIDADOR DE SEMANAS DE GESTACIÓN
# ====================================================================

def validar_semanas_gestacion(semanas):
    """
    Valida semanas de gestación.
    Rango: 1-42 semanas
    
    Args:
        semanas (int): Semanas de gestación
    
    Returns:
        tuple: (es_valida: bool, mensaje: str)
    """
    
    try:
        semanas = int(semanas)
    except (ValueError, TypeError):
        return False, 'Las semanas deben ser un número'
    
    if semanas < 1 or semanas > 42:
        return False, 'Las semanas deben estar entre 1-42'
    
    return True, 'Semanas válidas'


# ====================================================================
# VALIDADOR GENÉRICO DE RANGO
# ====================================================================

def validar_rango(valor, minimo, maximo, nombre_campo=''):
    """
    Valida que un valor esté dentro de un rango.
    
    Args:
        valor: Valor a validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        nombre_campo: Nombre del campo (para mensaje)
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return False, f'{nombre_campo} debe ser un número'
    
    if valor < minimo or valor > maximo:
        return False, f'{nombre_campo} debe estar entre {minimo}-{maximo}'
    
    return True, f'{nombre_campo} válido'


# ====================================================================
# VALIDADOR DE DESCRIPCIÓN
# ====================================================================

def validar_descripcion(descripcion, minimo=5, maximo=500):
    """
    Valida una descripción de texto.
    
    Args:
        descripcion (str): Texto a validar
        minimo (int): Longitud mínima
        maximo (int): Longitud máxima
    
    Returns:
        tuple: (es_valida: bool, mensaje: str)
    """
    
    if not descripcion or not isinstance(descripcion, str):
        return False, 'La descripción es requerida'
    
    descripcion = descripcion.strip()
    longitud = len(descripcion)
    
    if longitud < minimo:
        return False, f'La descripción debe tener al menos {minimo} caracteres'
    
    if longitud > maximo:
        return False, f'La descripción no puede exceder {maximo} caracteres'
    
    return True, 'Descripción válida'
