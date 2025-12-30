"""
Serializers para Productos

Estos serializers solo manejan la entrada/salida de datos HTTP.
La lógica de negocio está en la capa de dominio.
"""
from rest_framework import serializers
from apps.productos.models import Producto, PrecioProducto
from apps.empresas.api.serializers import EmpresaListSerializer


class PrecioInputSerializer(serializers.Serializer):
    """Serializer para entrada de precios"""
    moneda = serializers.CharField(max_length=3)
    precio = serializers.DecimalField(max_digits=15, decimal_places=2)


class PrecioOutputSerializer(serializers.Serializer):
    """Serializer para salida de precios"""
    id = serializers.IntegerField(allow_null=True)
    moneda = serializers.CharField()
    precio = serializers.FloatField()


class ProductoInputSerializer(serializers.Serializer):
    """Serializer para entrada de datos de Producto"""
    codigo = serializers.CharField(max_length=50)
    nombre = serializers.CharField(max_length=200)
    caracteristicas = serializers.CharField(required=False, allow_blank=True)
    empresa = serializers.CharField(max_length=20)  # NIT de la empresa
    precios = PrecioInputSerializer(many=True, required=False)


class ProductoOutputSerializer(serializers.Serializer):
    """Serializer para salida de datos de Producto"""
    id = serializers.IntegerField()
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    caracteristicas = serializers.CharField()
    empresa = serializers.CharField()
    empresa_nombre = serializers.CharField()
    precios = PrecioOutputSerializer(many=True)
    created_at = serializers.CharField(allow_null=True)
    updated_at = serializers.CharField(allow_null=True)


class ProductoListOutputSerializer(serializers.Serializer):
    """Serializer simplificado para listados"""
    id = serializers.IntegerField()
    codigo = serializers.CharField()
    nombre = serializers.CharField()
    caracteristicas = serializers.CharField()
    empresa = serializers.CharField()
    empresa_nombre = serializers.CharField()
    precios = PrecioOutputSerializer(many=True)


# Mantenemos compatibilidad con código existente
class PrecioProductoSerializer(serializers.ModelSerializer):
    """Serializer para precios de productos - Compatibilidad"""

    class Meta:
        model = PrecioProducto
        fields = ['id', 'moneda', 'precio']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto - Compatibilidad"""
    precios = PrecioProductoSerializer(many=True, required=False)

    class Meta:
        model = Producto
        fields = [
            'id', 'codigo', 'nombre', 'caracteristicas',
            'empresa', 'precios', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        precios_data = validated_data.pop('precios', [])
        producto = Producto.objects.create(**validated_data)
        for precio_data in precios_data:
            PrecioProducto.objects.create(producto=producto, **precio_data)
        return producto

    def update(self, instance, validated_data):
        precios_data = validated_data.pop('precios', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if precios_data is not None:
            instance.precios.all().delete()
            for precio_data in precios_data:
                PrecioProducto.objects.create(producto=instance, **precio_data)

        return instance


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados - Compatibilidad"""
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    precio_cop = serializers.SerializerMethodField()
    precios = PrecioProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'caracteristicas', 'empresa', 'empresa_nombre', 'precio_cop', 'precios']

    def get_precio_cop(self, obj):
        precio = obj.precios.filter(moneda='COP').first()
        return float(precio.precio) if precio else None


class ProductoDetailSerializer(serializers.ModelSerializer):
    """Serializer con todos los detalles - Compatibilidad"""
    precios = PrecioProductoSerializer(many=True, read_only=True)
    empresa_detail = EmpresaListSerializer(source='empresa', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'codigo', 'nombre', 'caracteristicas',
            'empresa', 'empresa_detail', 'precios',
            'created_at', 'updated_at'
        ]
