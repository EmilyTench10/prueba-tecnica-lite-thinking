# Domain - Capa de Dominio

Paquete Python independiente que contiene las entidades de dominio (modelos Django) para el sistema Lite Thinking.

## Arquitectura Limpia

Este paquete implementa la capa de dominio siguiendo los principios de Arquitectura Limpia:

- **Independencia**: El dominio es un paquete Python independiente, gestionado con Poetry
- **Modelos Django**: Utiliza modelos Django para mantener integridad referencial y relaciones FK
- **Sin dependencias de infraestructura**: No contiene vistas, serializers, controladores ni lógica HTTP
- **Reglas de negocio**: Contiene las entidades del negocio y sus reglas de validación

## Estructura

```
domain/
├── pyproject.toml          # Configuración Poetry con Django como dependencia
├── README.md
└── domain/                 # Paquete Python
    ├── __init__.py
    ├── apps.py             # Configuración Django App
    ├── exceptions.py       # Excepciones de dominio
    └── models/             # Modelos de dominio (entidades)
        ├── __init__.py
        ├── empresa.py      # Modelo Empresa
        ├── producto.py     # Modelos Producto y PrecioProducto
        ├── inventario.py   # Modelo Inventario
        └── usuario.py      # Modelo User personalizado
```

## Instalación

Este paquete se instala en el backend como dependencia local mediante Poetry:

```bash
cd backend
poetry add ../domain
```

O en el pyproject.toml del backend:

```toml
[tool.poetry.dependencies]
domain = {path = "../domain", develop = true}
```

## Uso

Desde el backend, los modelos se importan directamente:

```python
from domain.models import Empresa, Producto, Inventario, User
from domain.exceptions import ValidationException, EntityNotFoundException
```

O desde las apps del backend (que re-exportan los modelos):

```python
from apps.empresas.models import Empresa
from apps.productos.models import Producto, PrecioProducto
```

## Compatibilidad con Migraciones

Los modelos usan `app_label` para mantener compatibilidad con las migraciones existentes:

- `Empresa` → app_label = 'empresas'
- `Producto`, `PrecioProducto` → app_label = 'productos'
- `Inventario` → app_label = 'inventario'
- `User` → app_label = 'users'

Esto permite que las migraciones existentes sigan funcionando sin cambios.

## Principios Cumplidos

### h) Arquitectura Limpia

- Los modelos están en una capa de dominio **independiente del Backend**
- Desarrollada en **Python y Django**
- **Desacoplada** de vistas, serializers, controladores y lógica HTTP
- El Backend consume el dominio como un paquete externo

### i) Gestión de dependencias con Poetry

- El paquete tiene su propio `pyproject.toml`
- Django es una dependencia explícita del dominio
- El backend instala el dominio como dependencia local

## Notas Importantes

1. **Modificación de modelos**: Solo modificar los modelos en este paquete, nunca en el backend
2. **Migraciones**: Se generan desde el backend pero afectan los modelos de este paquete
3. **Sin lógica HTTP**: Este paquete NO debe contener vistas, URLs, serializers ni nada relacionado con HTTP/REST
