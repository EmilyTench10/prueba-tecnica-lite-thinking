from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings

from apps.inventario.models import Inventario
from apps.inventario.utils import generar_pdf_inventario
from apps.users.api.permissions import IsAdminRole, IsAdminOrReadOnly
from .serializers import InventarioSerializer, InventarioDetailSerializer, EnviarPDFSerializer


class InventarioViewSet(ModelViewSet):
    """
    ViewSet para CRUD de inventario
    - Admin: CRUD completo
    - Externo: solo lectura
    """
    queryset = Inventario.objects.all().select_related('empresa', 'producto')
    serializer_class = InventarioSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InventarioDetailSerializer
        return InventarioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'por_empresa']:
            return [AllowAny()]
        return [IsAdminRole()]

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """Obtener inventario filtrado por empresa"""
        empresa_nit = request.query_params.get('nit')
        if not empresa_nit:
            return Response(
                {'error': 'Se requiere el parámetro nit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        inventarios = self.queryset.filter(empresa__nit=empresa_nit)
        serializer = InventarioDetailSerializer(inventarios, many=True)
        return Response(serializer.data)


class DescargarPDFView(APIView):
    """Vista para descargar PDF del inventario"""
    permission_classes = [AllowAny]

    def get(self, request):
        empresa_nit = request.query_params.get('nit')
        pdf_buffer = generar_pdf_inventario(empresa_nit)

        filename = f"inventario_{empresa_nit or 'general'}.pdf"
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class EnviarPDFEmailView(APIView):
    """Vista para enviar PDF por email"""
    permission_classes = [IsAdminRole]

    def post(self, request):
        serializer = EnviarPDFSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email_destino = serializer.validated_data['email']
        empresa_nit = serializer.validated_data.get('empresa_nit')

        # Generar PDF
        pdf_buffer = generar_pdf_inventario(empresa_nit)

        # Crear email
        subject = f"Reporte de Inventario - {'Empresa ' + empresa_nit if empresa_nit else 'General'}"
        body = """
        Estimado usuario,

        Adjunto encontrará el reporte de inventario solicitado.

        Saludos,
        Sistema Lite Thinking
        """

        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.EMAIL_HOST_USER or 'noreply@litethinking.com',
                to=[email_destino]
            )

            filename = f"inventario_{empresa_nit or 'general'}.pdf"
            email.attach(filename, pdf_buffer.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            return Response({
                'message': f'PDF enviado exitosamente a {email_destino}',
                'email': email_destino
            })
        except Exception as e:
            return Response({
                'error': f'Error al enviar email: {str(e)}',
                'detail': 'Verifique la configuración de email en el servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
