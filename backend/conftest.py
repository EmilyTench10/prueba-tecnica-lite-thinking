"""
Configuracion de pytest para el proyecto.
"""
import os
import sys
import django
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user_admin(db):
    """Fixture que crea un usuario administrador"""
    User = get_user_model()
    return User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        role='admin'
    )


@pytest.fixture
def user_externo(db):
    """Fixture que crea un usuario externo"""
    User = get_user_model()
    return User.objects.create_user(
        email='externo@test.com',
        password='testpass123',
        role='externo'
    )


@pytest.fixture
def empresa_data():
    """Fixture con datos de empresa de prueba"""
    return {
        'nit': '123456789-1',
        'nombre': 'Empresa de Prueba',
        'direccion': 'Calle 123 #45-67',
        'telefono': '3001234567'
    }


@pytest.fixture
def producto_data():
    """Fixture con datos de producto de prueba"""
    return {
        'codigo': 'PROD-001',
        'nombre': 'Producto de Prueba',
        'caracteristicas': 'Caracteristicas del producto',
        'precios': [
            {'moneda': 'COP', 'precio': 50000},
            {'moneda': 'USD', 'precio': 12.50}
        ]
    }
