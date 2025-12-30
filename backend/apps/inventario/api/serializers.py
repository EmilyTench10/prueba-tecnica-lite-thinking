"""
Serializers para Inventario

Estos serializers solo manejan la entrada/salida de datos HTTP.
La lógica de negocio está en la capa de dominio.
"""
from rest_framework import serializers
from apps.inventario.models import Inventario
from apps.empresas.api.serializers import EmpresaListSerializer
from apps.productos.api.serializers import ProductoListSerializer


class InventarioInputSerializer(serializers.Serializer):
    """Serializer para entrada de datos de Inventario"""
    empresa = serializers.CharField(max_length=20)  # NIT
    producto = serializers.CharField(max_length=50)  # Código
    cantidad = serializers.IntegerField(min_value=0)
    ubicacion = serializers.CharField(max_length=100, required=False, allow_blank=True)


class InventarioOutputSerializer(serializers.Serializer):
    """Serializer para salida de datos de Inventario"""
    id = serializers.IntegerField()
    empresa = serializers.CharField()
    empresa_nombre = serializers.CharField()
    producto = serializers.CharField()
    producto_nombre = serializers.CharField()
    cantidad = serializers.IntegerField()
    ubicacion = serializers.CharField()
    created_at = serializers.CharField(allow_null=True)
    updated_at = serializers.CharField(allow_null=True)


class InventarioListOutputSerializer(serializers.Serializer):
    """Serializer simplificado para listados"""
    id = serializers.IntegerField()
    empresa = serializers.CharField()
    empresa_nombre = serializers.CharField()
    producto = serializers.CharField()
    producto_nombre = serializers.CharField()
    cantidad = serializers.IntegerField()
    ubicacion = serializers.CharField()


class EnviarPDFSerializer(serializers.Serializer):
    """Serializer para envío de PDF por email"""
    email = serializers.EmailField(required=True)
    empresa_nit = serializers.CharField(required=False, allow_blank=True, allow_null=True)


# Mantenemos compatibilidad con código existente
class InventarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inventario - Compatibilidad"""

    class Meta:
        model = Inventario
        fields = [
            'id', 'empresa', 'producto', 'cantidad',
            'ubicacion', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class InventarioDetailSerializer(serializers.ModelSerializer):
    """Serializer con detalles de empresa y producto - Compatibilidad"""
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
