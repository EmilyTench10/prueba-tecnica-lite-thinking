"""
Serializers para Empresas

Estos serializers solo manejan la entrada/salida de datos HTTP.
La lógica de negocio está en la capa de dominio.
"""
from rest_framework import serializers

# Importamos el modelo solo para serializers de compatibilidad
from apps.empresas.models import Empresa


class EmpresaInputSerializer(serializers.Serializer):
    """
    Serializer para entrada de datos de Empresa.
    Desacoplado del modelo - solo valida estructura de datos.
    """
    nit = serializers.CharField(max_length=20)
    nombre = serializers.CharField(max_length=200)
    direccion = serializers.CharField(max_length=300)
    telefono = serializers.CharField(max_length=20)


class EmpresaOutputSerializer(serializers.Serializer):
    """
    Serializer para salida de datos de Empresa.
    Mapea desde DTO a respuesta JSON.
    """
    nit = serializers.CharField()
    nombre = serializers.CharField()
    direccion = serializers.CharField()
    telefono = serializers.CharField()
    created_at = serializers.CharField(allow_null=True)
    updated_at = serializers.CharField(allow_null=True)


class EmpresaListOutputSerializer(serializers.Serializer):
    """Serializer simplificado para listados"""
    nit = serializers.CharField()
    nombre = serializers.CharField()
    direccion = serializers.CharField()
    telefono = serializers.CharField()


# Mantenemos compatibilidad con código existente
class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Empresa - Compatibilidad"""

    class Meta:
        model = Empresa
        fields = ['nit', 'nombre', 'direccion', 'telefono', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados - Compatibilidad"""

    class Meta:
        model = Empresa
        fields = ['nit', 'nombre', 'direccion', 'telefono']
