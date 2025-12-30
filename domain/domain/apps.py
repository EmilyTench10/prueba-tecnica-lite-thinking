"""
Configuración de la aplicación Django para el dominio.
"""
from django.apps import AppConfig


class DomainConfig(AppConfig):
    """Configuración de la app de dominio"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domain'
    verbose_name = 'Dominio Lite Thinking'
    label = 'domain'
