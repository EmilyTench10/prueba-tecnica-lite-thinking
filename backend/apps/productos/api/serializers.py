from rest_framework import serializers
from apps.productos.models import Producto, PrecioProducto
from apps.empresas.api.serializers import EmpresaListSerializer


class PrecioProductoSerializer(serializers.ModelSerializer):
    """Serializer para precios de productos"""

    class Meta:
        model = PrecioProducto
        fields = ['id', 'moneda', 'precio']


class ProductoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Producto"""
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
            # Eliminar precios existentes y crear nuevos
            instance.precios.all().delete()
            for precio_data in precios_data:
                PrecioProducto.objects.create(producto=instance, **precio_data)

        return instance


class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados"""
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
    """Serializer con todos los detalles"""
    precios = PrecioProductoSerializer(many=True, read_only=True)
    empresa_detail = EmpresaListSerializer(source='empresa', read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'codigo', 'nombre', 'caracteristicas',
            'empresa', 'empresa_detail', 'precios',
            'created_at', 'updated_at'
        ]
