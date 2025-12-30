# Lite Thinking Backend

API REST para el sistema de gestion de empresas, productos e inventario.

## Tecnologias

- **Django 5.0** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos
- **Poetry** - Gestion de dependencias
- **Clean Architecture** - Arquitectura del proyecto

## Estructura

```
backend/
├── domain/           # Paquete de dominio (Poetry)
├── infrastructure/   # Implementaciones (repositorios)
├── application/      # Casos de uso
├── apps/             # Apps de Django (presentacion)
├── config/           # Configuracion Django
└── tests/            # Tests unitarios
```

## Instalacion

```bash
# Instalar dependencias con Poetry
poetry install

# Activar entorno virtual
poetry shell

# Migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

## Tests

```bash
poetry run pytest tests/
```

## Arquitectura

El proyecto implementa Clean Architecture:

1. **Domain** - Entidades y reglas de negocio (paquete Poetry independiente)
2. **Application** - Casos de uso
3. **Infrastructure** - Repositorios con Django ORM
4. **Presentation** - Views y Serializers de DRF
