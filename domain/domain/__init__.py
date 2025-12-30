"""
Domain - Capa de Dominio
========================

Paquete Python independiente que contiene las entidades de dominio
(modelos Django) para el sistema Lite Thinking.

Este paquete sigue los principios de Arquitectura Limpia:
- Independiente del backend
- Sin dependencias de infraestructura (vistas, serializers, etc.)
- Contiene solo modelos y reglas de negocio

Uso:
    from domain.models import Empresa, Producto, Inventario, User
    from domain.exceptions import ValidationException, EntityNotFoundException
"""

__version__ = "1.0.0"

default_app_config = 'domain.apps.DomainConfig'

# Exportaciones principales
from domain.exceptions import (
    DomainException,
    EntityNotFoundException,
    ValidationException,
    BusinessRuleViolationException,
    DuplicateEntityException,
)

__all__ = [
    'DomainException',
    'EntityNotFoundException',
    'ValidationException',
    'BusinessRuleViolationException',
    'DuplicateEntityException',
]
