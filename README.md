# GruPero

Sistema web para registro y formación de grupos de trabajo, desarrollado con Flask y Bootstrap 5.

## Estructura del proyecto

```
grupero/
├── run.py                   # Punto de entrada
├── config.py                # Configuración por entornos
├── requirements.txt
├── .gitignore
├── data/                    # Generada automáticamente (no versionada)
│   └── personas.json
└── app/
    ├── __init__.py          # Factory (create_app)
    ├── models/
    │   ├── __init__.py
    │   └── persona.py       # Modelo Persona
    ├── main/                # Blueprint: inicio
    │   ├── __init__.py
    │   └── routes.py
    ├── persona/             # Blueprint: registro de personas
    │   ├── __init__.py
    │   ├── routes.py
    │   └── services.py
    ├── grupo/               # Blueprint: formación de grupos
    │   ├── __init__.py
    │   ├── routes.py
    │   └── services.py
    └── templates/
        ├── base.html
        ├── main/
        │   └── index.html
        ├── persona/
        │   └── index.html
        └── grupo/
            └── index.html
```

## Instalación y uso

```bash
pip install -r requirements.txt
python run.py
```

Abrí el navegador en: **http://localhost:5000**

## Funcionalidades

### Personas
- Registrar nombre, apellido y horarios disponibles
- Listar todas las personas registradas
- Eliminar personas

### Grupos
- Elegir tamaño del grupo
- **Al Azar:** selección aleatoria
- **Por Compatibilidad:** maximiza horarios en común
- **Manual:** elegís vos quiénes integran el grupo
- Muestra horarios en común del grupo resultante
