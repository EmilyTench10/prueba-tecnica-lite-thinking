"""
Excepciones de Dominio
======================

Estas excepciones representan errores en la lógica de negocio
y son parte de la capa de dominio.
"""
from typing import Optional, Dict, Any


class DomainException(Exception):
    """Excepción base para errores de dominio"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundException(DomainException):
    """Se lanza cuando no se encuentra una entidad"""

    def __init__(self, entity_name: str, identifier: Any):
        message = f"{entity_name} con identificador '{identifier}' no encontrado"
        super().__init__(message, {'entity': entity_name, 'identifier': identifier})


class ValidationException(DomainException):
    """Se lanza cuando hay errores de validación en el dominio"""

    def __init__(self, message: str, field: Optional[str] = None):
        details = {'field': field} if field else {}
        super().__init__(message, details)


class BusinessRuleViolationException(DomainException):
    """Se lanza cuando se viola una regla de negocio"""

    def __init__(self, rule: str, message: str):
        super().__init__(message, {'rule': rule})


class DuplicateEntityException(DomainException):
    """Se lanza cuando se intenta crear una entidad duplicada"""

    def __init__(self, entity_name: str, identifier: Any):
        message = f"{entity_name} con identificador '{identifier}' ya existe"
        super().__init__(message, {'entity': entity_name, 'identifier': identifier})
