# 🏥 Obstetric Care v2 - Guía de Instalación

## ⚠️ ATENCIÓN: Lee esto antes de empezar

Este es un proyecto en grupo. Sigue los pasos exactamente en orden.

## Paso 1: Clonar o descargar el proyecto
```bash
git clone <URL del repositorio>
cd obstetric_care_v2
```

## Paso 2: Crear el ambiente virtual

### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Paso 3: Instalar dependencias

Con el ambiente virtual **activado**, ejecuta:
```bash
pip install -r requirements.txt
```

## Paso 4: Migraciones de base de datos
```bash
python manage.py migrate
```

## Paso 5: Crear superusuario (solo la primera vez)
```bash
python manage.py createsuperuser
```

## Paso 6: Ejecutar el servidor
```bash
python manage.py runserver
```

El servidor estará en: `http://localhost:8000`

---

## ✅ Verificación

Si ves el cohete de Django en `http://localhost:8000`, ¡todo está bien!

## ⚠️ Si algo falla

1. Verifica que el ambiente virtual esté **activado** (debe decir `(venv)` al inicio de la línea)
2. Verifica que estés en la carpeta correcta (donde está `manage.py`)
3. Ejecuta: `pip list` para ver las dependencias instaladas