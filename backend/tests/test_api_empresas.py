"""
Tests de integracion para la API de Empresas.

Estos tests verifican que la API funciona correctamente
de punta a punta.
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from apps.empresas.models import Empresa


@pytest.fixture
def api_client():
    """Cliente de API para tests"""
    return APIClient()


@pytest.fixture
def api_client_admin(api_client, user_admin):
    """Cliente de API autenticado como admin"""
    api_client.force_authenticate(user=user_admin)
    return api_client


@pytest.fixture
def api_client_externo(api_client, user_externo):
    """Cliente de API autenticado como externo"""
    api_client.force_authenticate(user=user_externo)
    return api_client


@pytest.fixture
def empresa_existente(db):
    """Fixture que crea una empresa en la BD"""
    return Empresa.objects.create(
        nit='999888777-1',
        nombre='Empresa Existente',
        direccion='Direccion existente',
        telefono='3009999999'
    )


@pytest.mark.django_db
class TestEmpresaAPI:
    """Tests para el endpoint de Empresas"""

    def test_listar_empresas_sin_autenticacion(self, api_client, empresa_existente):
        """Test: Cualquier usuario puede listar empresas"""
        response = api_client.get('/api/empresas/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_obtener_empresa_por_nit(self, api_client, empresa_existente):
        """Test: Obtener empresa por NIT"""
        response = api_client.get(f'/api/empresas/{empresa_existente.nit}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nit'] == empresa_existente.nit

    def test_crear_empresa_como_admin(self, api_client_admin, empresa_data):
        """Test: Admin puede crear empresa"""
        response = api_client_admin.post('/api/empresas/', empresa_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['nit'] == empresa_data['nit']
        assert response.data['nombre'] == empresa_data['nombre']

    def test_crear_empresa_sin_autenticacion_falla(self, api_client, empresa_data):
        """Test: Usuario no autenticado no puede crear empresa"""
        response = api_client.post('/api/empresas/', empresa_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_crear_empresa_como_externo_falla(self, api_client_externo, empresa_data):
        """Test: Usuario externo no puede crear empresa"""
        response = api_client_externo.post('/api/empresas/', empresa_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_crear_empresa_duplicada_falla(self, api_client_admin, empresa_existente):
        """Test: No se puede crear empresa con NIT duplicado"""
        data = {
            'nit': empresa_existente.nit,  # NIT ya existe
            'nombre': 'Otra Empresa',
            'direccion': 'Otra Direccion',
            'telefono': '3001111111'
        }
        response = api_client_admin.post('/api/empresas/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'ya existe' in response.data['error'].lower()

    def test_actualizar_empresa_como_admin(self, api_client_admin, empresa_existente):
        """Test: Admin puede actualizar empresa"""
        data = {'nombre': 'Nombre Actualizado'}
        response = api_client_admin.patch(
            f'/api/empresas/{empresa_existente.nit}/',
            data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nombre'] == 'Nombre Actualizado'

    def test_actualizar_empresa_como_externo_falla(self, api_client_externo, empresa_existente):
        """Test: Usuario externo no puede actualizar empresa"""
        data = {'nombre': 'Nombre Actualizado'}
        response = api_client_externo.patch(
            f'/api/empresas/{empresa_existente.nit}/',
            data
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_eliminar_empresa_como_admin(self, api_client_admin, empresa_existente):
        """Test: Admin puede eliminar empresa"""
        response = api_client_admin.delete(
            f'/api/empresas/{empresa_existente.nit}/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Empresa.objects.filter(nit=empresa_existente.nit).exists()

    def test_eliminar_empresa_como_externo_falla(self, api_client_externo, empresa_existente):
        """Test: Usuario externo no puede eliminar empresa"""
        response = api_client_externo.delete(
            f'/api/empresas/{empresa_existente.nit}/'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_obtener_empresa_inexistente(self, api_client):
        """Test: Obtener empresa que no existe retorna 404"""
        response = api_client.get('/api/empresas/999999999-9/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_crear_empresa_sin_nit_falla(self, api_client_admin):
        """Test: Crear empresa sin NIT falla"""
        data = {
            'nombre': 'Empresa Sin NIT',
            'direccion': 'Direccion',
            'telefono': '3001234567'
        }
        response = api_client_admin.post('/api/empresas/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
