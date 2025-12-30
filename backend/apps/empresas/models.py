"""
Re-exportación de modelos desde la capa de dominio.

Los modelos reales están en el paquete domain (capa de dominio independiente).
Este archivo mantiene compatibilidad con imports existentes.
"""
from domain.models import Empresa

__all__ = ['Empresa']
