import requests
import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

from apps.chatbot.models import ConversacionChat, MensajeChat
from .serializers import (
    ConversacionChatSerializer,
    MensajeChatSerializer,
    EnviarMensajeSerializer
)


class ChatbotView(APIView):
    """Vista para interactuar con el chatbot de n8n"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EnviarMensajeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mensaje = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())

        # Obtener o crear conversación
        conversacion, _ = ConversacionChat.objects.get_or_create(
            session_id=session_id,
            defaults={'usuario': request.user if request.user.is_authenticated else None}
        )

        # Guardar mensaje del usuario
        MensajeChat.objects.create(
            conversacion=conversacion,
            tipo='user',
            mensaje=mensaje
        )

        # Llamar al webhook de n8n
        try:
            webhook_url = settings.CHATBOT_WEBHOOK_URL
            payload = {"message": mensaje}
            headers = {"Content-Type": "application/json"}

            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                # Intentar obtener respuesta como JSON o texto
                try:
                    bot_response = response.json()
                    if isinstance(bot_response, dict):
                        respuesta = bot_response.get('response', bot_response.get('message', str(bot_response)))
                    else:
                        respuesta = str(bot_response)
                except:
                    respuesta = response.text

                # Guardar respuesta del bot
                MensajeChat.objects.create(
                    conversacion=conversacion,
                    tipo='bot',
                    mensaje=respuesta
                )

                return Response({
                    'session_id': session_id,
                    'response': respuesta,
                    'success': True
                })
            else:
                # Fallback: respuesta local
                respuesta = self._get_fallback_response(mensaje)
                MensajeChat.objects.create(
                    conversacion=conversacion,
                    tipo='bot',
                    mensaje=respuesta
                )
                return Response({
                    'session_id': session_id,
                    'response': respuesta,
                    'success': True
                })

        except (requests.exceptions.Timeout, requests.exceptions.RequestException):
            # Fallback: respuesta local cuando n8n no está disponible
            respuesta = self._get_fallback_response(mensaje)
            MensajeChat.objects.create(
                conversacion=conversacion,
                tipo='bot',
                mensaje=respuesta
            )
            return Response({
                'session_id': session_id,
                'response': respuesta,
                'success': True
            })

    def _get_fallback_response(self, mensaje):
        """Genera respuestas locales cuando n8n no está disponible"""
        mensaje_lower = mensaje.lower()

        if any(word in mensaje_lower for word in ['hola', 'buenos', 'buenas', 'hey', 'hi']):
            return "¡Hola! Soy el asistente virtual de Lite Thinking. ¿En qué puedo ayudarte hoy? Puedo informarte sobre empresas, productos, inventario o el sistema en general."

        elif any(word in mensaje_lower for word in ['empresa', 'empresas', 'compañía', 'nit']):
            return "El módulo de Empresas te permite gestionar las compañías registradas. Puedes agregar empresas con su NIT, nombre, dirección y teléfono. Solo los administradores pueden crear, editar o eliminar empresas."

        elif any(word in mensaje_lower for word in ['producto', 'productos', 'catálogo', 'precio']):
            return "El módulo de Productos te permite gestionar el catálogo con precios en múltiples monedas (USD, EUR, COP). Cada producto está asociado a una empresa y tiene código único, nombre, características y precios."

        elif any(word in mensaje_lower for word in ['inventario', 'stock', 'cantidad', 'pdf', 'email']):
            return "El módulo de Inventario te permite controlar el stock de productos. Puedes descargar reportes en PDF y enviarlos por correo electrónico. Se registra cada movimiento de inventario."

        elif any(word in mensaje_lower for word in ['blockchain', 'integridad', 'hash', 'verificar']):
            return "El módulo de Blockchain verifica la integridad de los datos mediante hashes SHA-256. Cada registro de inventario se almacena en una cadena de bloques para garantizar trazabilidad y seguridad."

        elif any(word in mensaje_lower for word in ['usuario', 'admin', 'rol', 'permiso', 'login']):
            return "El sistema tiene dos roles: Administrador (acceso completo a CRUD) y Externo (solo lectura). Los usuarios se autentican con email y contraseña encriptada mediante JWT."

        elif any(word in mensaje_lower for word in ['ayuda', 'help', 'qué puedes', 'funciones']):
            return "Puedo ayudarte con información sobre:\n• Gestión de Empresas\n• Catálogo de Productos\n• Control de Inventario\n• Verificación Blockchain\n• Usuarios y permisos\n\n¿Sobre qué tema te gustaría saber más?"

        elif any(word in mensaje_lower for word in ['gracias', 'thanks', 'genial', 'perfecto']):
            return "¡De nada! Estoy aquí para ayudarte. ¿Hay algo más en lo que pueda asistirte?"

        elif any(word in mensaje_lower for word in ['adiós', 'chao', 'bye', 'hasta luego']):
            return "¡Hasta pronto! Fue un placer ayudarte. Vuelve cuando necesites asistencia."

        else:
            return "Entiendo tu consulta. Soy el asistente de Lite Thinking y puedo ayudarte con información sobre empresas, productos, inventario, blockchain y usuarios. ¿Podrías ser más específico sobre lo que necesitas?"


class ConversacionViewSet(ReadOnlyModelViewSet):
    """ViewSet para ver historial de conversaciones"""
    serializer_class = ConversacionChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar conversaciones del usuario autenticado
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return ConversacionChat.objects.all()
            return ConversacionChat.objects.filter(usuario=self.request.user)
        return ConversacionChat.objects.none()


class HistorialChatView(APIView):
    """Vista para obtener historial de una sesión específica"""
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        try:
            conversacion = ConversacionChat.objects.get(session_id=session_id)
            serializer = ConversacionChatSerializer(conversacion)
            return Response(serializer.data)
        except ConversacionChat.DoesNotExist:
            return Response(
                {'error': 'Conversación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
