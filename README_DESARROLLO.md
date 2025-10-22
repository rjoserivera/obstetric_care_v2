# 🏥 Obstetric Care v2 - Guía de Desarrollo

## Estructura del Proyecto
```
obstetric_care_v2/
├── obstetric_care_v2/        # Configuración principal
│   ├── settings.py           # Configuración de Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py
├── apps/
│   ├── core/                 # Modelos base (Persona)
│   ├── admision/             # Ingreso de personas
│   ├── pacientes/            # Fichas clínicas y controles
│   ├── registros/            # Observaciones, patologías, procedimientos
│   └── personal/             # Perfiles y usuarios
├── templates/                # Templates HTML por app
│   ├── core/
│   ├── admision/
│   ├── pacientes/
│   ├── registros/
│   └── personal/
├── static/                   # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── utilidades/               # Funciones auxiliares
│   └── validador_rut.js
├── manage.py
└── requirements.txt
```

## Modelos y Relaciones

### Core
- **Persona**: Registro base de cualquier persona (madre)
  - RUT, nombre, edad, contacto

### Admisión
- **Admision**: Vinculada a Persona
  - Previsión (FONASA, ISAPRE, etc)
  - Estado (activo/inactivo)

### Pacientes
- **Paciente**: Vinculada a Persona (madre)
  - Número de ficha
  - Antecedentes obstétricos
  - Patologías
- **ControlPrenatal**: Vinculado a Paciente
  - Fecha control, semanas gestación, peso, presión

### Registros
- **Observacion**: Notas médicas
- **Patologia**: Patologías del paciente
- **Procedimiento**: Procedimientos realizados por TENS
- **Medicamento**: Medicamentos administrados

### Personal
- **Perfil**: Usuario con rol
  - Roles: Administrativo, Matrona, Médico, TENS

## Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **Administrativo** | Ingresa datos básicos de Persona |
| **Matrona** | Crea fichas, completa antecedentes, registra controles |
| **Médico** | Acceso total (lectura y escritura) |
| **TENS** | Registra procedimientos y medicamentos |

## Flujo de Trabajo

1. **Admisión**: Administrativo ingresa Persona
2. **Paciente**: Matrona crea Ficha vinculada a Persona
3. **Registros**: Cada profesional registra su actividad
4. **Consulta**: Todos acceden según sus permisos

## Convenciones de Código

### Comentarios
**JavaScript:**
```javascript
///////////////////////////////////
// Descripción de la función
///////////////////////////////////
function miFunction() {
    // código
}
```

**Python:**
```python
################
# Descripción
################
def mi_funcion():
    # código
```

### Nombres de Archivos
- Templates: `nombre_accion.html` (ej: `crear_paciente.html`)
- Vistas: `views.py`
- Modelos: `models.py`
- Admin: `admin.py`

### Nombres de Variables
- Python: `snake_case` (mi_variable)
- JavaScript: `camelCase` (miVariable)

## Comandos Útiles
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear usuario
python manage.py createsuperuser

# Servidor de desarrollo
python manage.py runserver

# Shell de Django
python manage.py shell

# Crear app
python manage.py startapp nombreapp
```

## Base de Datos

Actualmente usa **SQLite** para desarrollo. Para producción cambiar a **PostgreSQL** en `settings.py`.

## Notas Importantes

- Siempre activar el ambiente virtual antes de trabajar
- Hacer pull antes de empezar a trabajar
- Hacer commits pequeños y descriptivos
- Actualizar `requirements.txt` si instalas algo nuevo: `pip freeze > requirements.txt`

---

**Última actualización**: Octubre 2025