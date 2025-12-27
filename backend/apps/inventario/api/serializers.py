from rest_framework import serializers
from apps.inventario.models import Inventario
from apps.empresas.api.serializers import EmpresaListSerializer
from apps.productos.api.serializers import ProductoListSerializer


class InventarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inventario"""

    class Meta:
        model = Inventario
        fields = [
            'id', 'empresa', 'producto', 'cantidad',
            'ubicacion', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class InventarioDetailSerializer(serializers.ModelSerializer):
    """Serializer con detalles de empresa y producto"""
    empresa_detail = EmpresaListSerializer(source='empresa', read_only=True)
    producto_detail = ProductoListSerializer(source='producto', read_only=True)

    class Meta:
        model = Inventario
        fields = [
            'id', 'empresa', 'empresa_detail',
            'producto', 'producto_detail',
            'cantidad', 'ubicacion',
            'created_at', 'updated_at'
        ]


class EnviarPDFSerializer(serializers.Serializer):
    """Serializer para envío de PDF por email"""
    email = serializers.EmailField(required=True)
    empresa_nit = serializers.CharField(required=False, allow_blank=True, allow_null=True)
