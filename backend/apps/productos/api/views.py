from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from apps.productos.models import Producto, PrecioProducto
from apps.users.api.permissions import IsAdminOrReadOnly, IsAdminRole
from .serializers import (
    ProductoSerializer,
    ProductoListSerializer,
    ProductoDetailSerializer,
    PrecioProductoSerializer
)


class ProductoViewSet(ModelViewSet):
    """
    ViewSet para CRUD de productos
    - Admin: puede crear, editar, eliminar
    - Externo: solo puede ver (lectura)
    """
    queryset = Producto.objects.all().prefetch_related('precios')
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        if self.action == 'retrieve':
            return ProductoDetailSerializer
        return ProductoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminRole()]

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """Obtener productos filtrados por empresa"""
        empresa_nit = request.query_params.get('nit')
        if not empresa_nit:
            return Response(
                {'error': 'Se requiere el parámetro nit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        productos = self.queryset.filter(empresa__nit=empresa_nit)
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def agregar_precio(self, request, pk=None):
        """Agregar un precio en una moneda específica"""
        producto = self.get_object()
        serializer = PrecioProductoSerializer(data=request.data)

        if serializer.is_valid():
            # Verificar si ya existe precio para esa moneda
            moneda = serializer.validated_data['moneda']
            PrecioProducto.objects.filter(producto=producto, moneda=moneda).delete()
            serializer.save(producto=producto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
