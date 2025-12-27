from rest_framework import serializers
from apps.empresas.models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Empresa"""

    class Meta:
        model = Empresa
        fields = ['nit', 'nombre', 'direccion', 'telefono', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados"""

    class Meta:
        model = Empresa
        fields = ['nit', 'nombre', 'direccion', 'telefono']
