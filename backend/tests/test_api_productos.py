"""
Tests de integracion para la API de Productos.
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from apps.empresas.models import Empresa
from apps.productos.models import Producto, PrecioProducto


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_admin(api_client, user_admin):
    api_client.force_authenticate(user=user_admin)
    return api_client


@pytest.fixture
def empresa_para_producto(db):
    """Empresa necesaria para crear productos"""
    return Empresa.objects.create(
        nit='111222333-1',
        nombre='Empresa Para Productos',
        direccion='Direccion',
        telefono='3001234567'
    )


@pytest.fixture
def producto_existente(db, empresa_para_producto):
    """Producto existente en BD"""
    producto = Producto.objects.create(
        codigo='EXIST-001',
        nombre='Producto Existente',
        caracteristicas='Caracteristicas',
        empresa=empresa_para_producto
    )
    PrecioProducto.objects.create(
        producto=producto,
        moneda='COP',
        precio=50000
    )
    return producto


@pytest.mark.django_db
class TestProductoAPI:
    """Tests para el endpoint de Productos"""

    def test_listar_productos(self, api_client, producto_existente):
        """Test: Listar productos sin autenticacion"""
        response = api_client.get('/api/productos/')
        assert response.status_code == status.HTTP_200_OK

    def test_crear_producto_como_admin(self, api_client_admin, empresa_para_producto):
        """Test: Admin puede crear producto"""
        data = {
            'codigo': 'NEW-001',
            'nombre': 'Nuevo Producto',
            'caracteristicas': 'Descripcion del producto',
            'empresa': empresa_para_producto.nit,
            'precios': [
                {'moneda': 'COP', 'precio': 100000},
                {'moneda': 'USD', 'precio': 25}
            ]
        }
        response = api_client_admin.post('/api/productos/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['codigo'] == 'NEW-001'
        assert len(response.data['precios']) == 2

    def test_crear_producto_codigo_duplicado_falla(self, api_client_admin, producto_existente, empresa_para_producto):
        """Test: No se puede crear producto con codigo duplicado"""
        data = {
            'codigo': producto_existente.codigo,  # Ya existe
            'nombre': 'Otro Producto',
            'caracteristicas': 'Descripcion',
            'empresa': empresa_para_producto.nit
        }
        response = api_client_admin.post('/api/productos/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_crear_producto_empresa_inexistente_falla(self, api_client_admin):
        """Test: No se puede crear producto con empresa inexistente"""
        data = {
            'codigo': 'TEST-001',
            'nombre': 'Producto',
            'caracteristicas': 'Descripcion',
            'empresa': '000000000-0'  # No existe
        }
        response = api_client_admin.post('/api/productos/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_agregar_precio_a_producto(self, api_client_admin, producto_existente):
        """Test: Agregar precio a producto existente"""
        data = {
            'moneda': 'USD',
            'precio': 15.99
        }
        response = api_client_admin.post(
            f'/api/productos/{producto_existente.id}/agregar_precio/',
            data
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_obtener_productos_por_empresa(self, api_client, producto_existente, empresa_para_producto):
        """Test: Filtrar productos por empresa"""
        response = api_client.get(
            f'/api/productos/por_empresa/?nit={empresa_para_producto.nit}'
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
