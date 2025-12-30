"""
Views para Productos

Estas views solo manejan la capa HTTP.
La lógica de negocio está delegada a los casos de uso.
"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from apps.users.api.permissions import IsAdminOrReadOnly, IsAdminRole
from application.use_cases import ProductoUseCases
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException,
    BusinessRuleViolationException
)
from .serializers import (
    ProductoInputSerializer,
    ProductoOutputSerializer,
    ProductoListOutputSerializer,
    PrecioInputSerializer
)


class ProductoViewSet(ViewSet):
    """
    ViewSet para CRUD de productos usando Arquitectura Limpia.

    - Admin: puede crear, editar, eliminar
    - Externo: solo puede ver (lectura)
    """
    permission_classes = [IsAdminOrReadOnly]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_cases = ProductoUseCases()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'por_empresa']:
            return [AllowAny()]
        return [IsAdminRole()]

    def list(self, request):
        """GET /api/productos/ - Listar todos los productos"""
        try:
            productos = self._use_cases.listar_productos()
            serializer = ProductoListOutputSerializer(
                [p.to_dict() for p in productos],
                many=True
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """GET /api/productos/{id}/ - Obtener un producto"""
        try:
            producto = self._use_cases.obtener_producto(int(pk))
            serializer = ProductoOutputSerializer(producto.to_dict())
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
        """POST /api/productos/ - Crear un producto"""
        input_serializer = ProductoInputSerializer(data=request.data)

        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            precios = input_serializer.validated_data.get('precios', [])
            precios_dict = [{'moneda': p['moneda'], 'precio': float(p['precio'])} for p in precios]

            producto = self._use_cases.crear_producto(
                codigo=input_serializer.validated_data['codigo'],
                nombre=input_serializer.validated_data['nombre'],
                caracteristicas=input_serializer.validated_data.get('caracteristicas', ''),
                empresa_nit=input_serializer.validated_data['empresa'],
                precios=precios_dict if precios_dict else None
            )
            output_serializer = ProductoOutputSerializer(producto.to_dict())
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except DuplicateEntityException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        """PUT /api/productos/{id}/ - Actualizar un producto"""
        try:
            producto = self._use_cases.actualizar_producto(
                id=int(pk),
                nombre=request.data.get('nombre'),
                caracteristicas=request.data.get('caracteristicas')
            )

            # Actualizar precios si se proporcionan
            precios = request.data.get('precios', [])
            for precio in precios:
                self._use_cases.agregar_precio(
                    producto_id=int(pk),
                    monto=float(precio['precio']),
                    moneda=precio['moneda']
                )

            # Obtener producto actualizado
            producto = self._use_cases.obtener_producto(int(pk))
            output_serializer = ProductoOutputSerializer(producto.to_dict())
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

    def partial_update(self, request, pk=None):
        """PATCH /api/productos/{id}/ - Actualización parcial"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """DELETE /api/productos/{id}/ - Eliminar un producto"""
        try:
            self._use_cases.eliminar_producto(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """GET /api/productos/por_empresa/?nit=XXX - Productos por empresa"""
        empresa_nit = request.query_params.get('nit')
        if not empresa_nit:
            return Response(
                {'error': 'Se requiere el parámetro nit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            productos = self._use_cases.listar_por_empresa(empresa_nit)
            serializer = ProductoListOutputSerializer(
                [p.to_dict() for p in productos],
                many=True
            )
            return Response(serializer.data)
        except ValidationException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def agregar_precio(self, request, pk=None):
        """POST /api/productos/{id}/agregar_precio/ - Agregar precio"""
        serializer = PrecioInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            producto = self._use_cases.agregar_precio(
                producto_id=int(pk),
                monto=float(serializer.validated_data['precio']),
                moneda=serializer.validated_data['moneda']
            )
            output_serializer = ProductoOutputSerializer(producto.to_dict())
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except BusinessRuleViolationException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
