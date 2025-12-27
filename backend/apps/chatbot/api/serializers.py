from rest_framework import serializers
from apps.chatbot.models import ConversacionChat, MensajeChat


class MensajeChatSerializer(serializers.ModelSerializer):
    """Serializer para mensajes de chat"""

    class Meta:
        model = MensajeChat
        fields = ['id', 'tipo', 'mensaje', 'timestamp']
        read_only_fields = ['timestamp']


class ConversacionChatSerializer(serializers.ModelSerializer):
    """Serializer para conversaciones"""
    mensajes = MensajeChatSerializer(many=True, read_only=True)

    class Meta:
        model = ConversacionChat
        fields = ['id', 'session_id', 'usuario', 'created_at', 'mensajes']
        read_only_fields = ['created_at']


class EnviarMensajeSerializer(serializers.Serializer):
    """Serializer para enviar mensaje al chatbot"""
    message = serializers.CharField(required=True)
    session_id = serializers.CharField(required=False)
