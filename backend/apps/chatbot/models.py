from django.db import models
from apps.users.models import User


class ConversacionChat(models.Model):
    """Modelo para guardar historial de conversaciones con el chatbot"""

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversaciones',
        verbose_name='Usuario',
        null=True,
        blank=True
    )
    session_id = models.CharField('ID de Sesión', max_length=100)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversación {self.session_id}"


class MensajeChat(models.Model):
    """Modelo para mensajes individuales del chat"""

    TIPO_CHOICES = [
        ('user', 'Usuario'),
        ('bot', 'Bot'),
    ]

    conversacion = models.ForeignKey(
        ConversacionChat,
        on_delete=models.CASCADE,
        related_name='mensajes',
        verbose_name='Conversación'
    )
    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_CHOICES)
    mensaje = models.TextField('Mensaje')
    timestamp = models.DateTimeField('Marca de tiempo', auto_now_add=True)

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.tipo}: {self.mensaje[:50]}..."
