from rest_framework import serializers
from apps.blockchain.models import RegistroBlockchain


class RegistroBlockchainSerializer(serializers.ModelSerializer):
    """Serializer para registros blockchain"""

    class Meta:
        model = RegistroBlockchain
        fields = [
            'indice', 'tipo', 'datos', 'timestamp',
            'hash_anterior', 'hash_actual', 'usuario'
        ]
        read_only_fields = ['indice', 'hash_anterior', 'hash_actual', 'timestamp']


class VerificarIntegridadSerializer(serializers.Serializer):
    """Serializer para respuesta de verificación"""
    valido = serializers.BooleanField()
    total_bloques = serializers.IntegerField()
    errores = serializers.ListField(child=serializers.DictField())
