"""
Views para Empresas

Estas views solo manejan la capa HTTP.
La lógica de negocio está delegada a los casos de uso.
"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.api.permissions import IsAdminOrReadOnly, IsAdminRole
from application.use_cases import EmpresaUseCases
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException
)
from .serializers import (
    EmpresaInputSerializer,
    EmpresaOutputSerializer,
    EmpresaListOutputSerializer
)


class EmpresaViewSet(ViewSet):
    """
    ViewSet para CRUD de empresas usando Arquitectura Limpia.

    - Admin: puede crear, editar, eliminar
    - Externo: solo puede ver (lectura)

    La lógica de negocio está en la capa de dominio,
    esta vista solo maneja la capa HTTP.
    """
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'nit'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_cases = EmpresaUseCases()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminRole()]

    def list(self, request):
        """GET /api/empresas/ - Listar todas las empresas"""
        try:
            empresas = self._use_cases.listar_empresas()
            serializer = EmpresaListOutputSerializer(
                [e.to_dict() for e in empresas],
                many=True
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, nit=None):
        """GET /api/empresas/{nit}/ - Obtener una empresa"""
        try:
            empresa = self._use_cases.obtener_empresa(nit)
            serializer = EmpresaOutputSerializer(empresa.to_dict())
            return Response(serializer.data)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        """POST /api/empresas/ - Crear una empresa"""
        input_serializer = EmpresaInputSerializer(data=request.data)

        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            empresa = self._use_cases.crear_empresa(
                nit=input_serializer.validated_data['nit'],
                nombre=input_serializer.validated_data['nombre'],
                direccion=input_serializer.validated_data['direccion'],
                telefono=input_serializer.validated_data['telefono']
            )
            output_serializer = EmpresaOutputSerializer(empresa.to_dict())
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except DuplicateEntityException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, nit=None):
        """PUT /api/empresas/{nit}/ - Actualizar una empresa"""
        input_serializer = EmpresaInputSerializer(data=request.data, partial=True)

        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            empresa = self._use_cases.actualizar_empresa(
                nit=nit,
                nombre=input_serializer.validated_data.get('nombre'),
                direccion=input_serializer.validated_data.get('direccion'),
                telefono=input_serializer.validated_data.get('telefono')
            )
            output_serializer = EmpresaOutputSerializer(empresa.to_dict())
            return Response(output_serializer.data)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, nit=None):
        """PATCH /api/empresas/{nit}/ - Actualización parcial"""
        return self.update(request, nit)

    def destroy(self, request, nit=None):
        """DELETE /api/empresas/{nit}/ - Eliminar una empresa"""
        try:
            self._use_cases.eliminar_empresa(nit)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
