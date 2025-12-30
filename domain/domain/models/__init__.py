"""
Modelos de Dominio - Lite Thinking
==================================

Este paquete contiene todas las entidades del dominio como modelos Django.
Mantiene la integridad referencial y las relaciones entre entidades.
"""

from domain.models.empresa import Empresa
from domain.models.producto import Producto, PrecioProducto
from domain.models.inventario import Inventario
from domain.models.usuario import User, UserManager

__all__ = [
    'Empresa',
    'Producto',
    'PrecioProducto',
    'Inventario',
    'User',
    'UserManager',
]
