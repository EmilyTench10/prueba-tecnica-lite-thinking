"""
Views para Inventario

Estas views solo manejan la capa HTTP.
La lógica de negocio está delegada a los casos de uso.
"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings

from apps.inventario.utils import generar_pdf_inventario
from apps.users.api.permissions import IsAdminRole, IsAdminOrReadOnly
from application.use_cases import InventarioUseCases
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException,
    BusinessRuleViolationException
)
from .serializers import (
    InventarioInputSerializer,
    InventarioOutputSerializer,
    InventarioListOutputSerializer,
    EnviarPDFSerializer
)


class InventarioViewSet(ViewSet):
    """
    ViewSet para CRUD de inventario usando Arquitectura Limpia.

    - Admin: CRUD completo
    - Externo: solo lectura
    """
    permission_classes = [IsAdminOrReadOnly]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_cases = InventarioUseCases()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'por_empresa', 'estadisticas']:
            return [AllowAny()]
        return [IsAdminRole()]

    def list(self, request):
        """GET /api/inventario/ - Listar todo el inventario"""
        try:
            inventarios = self._use_cases.listar_inventario()
            serializer = InventarioListOutputSerializer(
                [i.to_dict() for i in inventarios],
                many=True
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """GET /api/inventario/{id}/ - Obtener un registro"""
        try:
            inventario = self._use_cases.obtener_registro(int(pk))
            serializer = InventarioOutputSerializer(inventario.to_dict())
            return Response(serializer.data)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """POST /api/inventario/ - Crear un registro"""
        input_serializer = InventarioInputSerializer(data=request.data)

        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            inventario = self._use_cases.crear_registro(
                empresa_nit=input_serializer.validated_data['empresa'],
                producto_codigo=input_serializer.validated_data['producto'],
                cantidad=input_serializer.validated_data['cantidad'],
                ubicacion=input_serializer.validated_data.get('ubicacion', '')
            )
            output_serializer = InventarioOutputSerializer(inventario.to_dict())
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except DuplicateEntityException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk=None):
        """PUT /api/inventario/{id}/ - Actualizar un registro"""
        try:
            inventario = self._use_cases.actualizar_registro(
                id=int(pk),
                cantidad=request.data.get('cantidad'),
                ubicacion=request.data.get('ubicacion')
            )
            output_serializer = InventarioOutputSerializer(inventario.to_dict())
            return Response(output_serializer.data)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationException as e:
            return Response(
                {'error': e.message, 'field': e.details.get('field')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk=None):
        """PATCH /api/inventario/{id}/ - Actualización parcial"""
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """DELETE /api/inventario/{id}/ - Eliminar un registro"""
        try:
            self._use_cases.eliminar_registro(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def por_empresa(self, request):
        """GET /api/inventario/por_empresa/?nit=XXX - Inventario por empresa"""
        empresa_nit = request.query_params.get('nit')
        if not empresa_nit:
            return Response(
                {'error': 'Se requiere el parámetro nit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            inventarios = self._use_cases.listar_por_empresa(empresa_nit)
            serializer = InventarioListOutputSerializer(
                [i.to_dict() for i in inventarios],
                many=True
            )
            return Response(serializer.data)
        except ValidationException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """GET /api/inventario/estadisticas/ - Estadísticas de inventario"""
        try:
            stats = self._use_cases.obtener_estadisticas()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def incrementar(self, request, pk=None):
        """POST /api/inventario/{id}/incrementar/ - Incrementar stock"""
        cantidad = request.data.get('cantidad', 0)
        try:
            inventario = self._use_cases.incrementar_stock(int(pk), int(cantidad))
            output_serializer = InventarioOutputSerializer(inventario.to_dict())
            return Response(output_serializer.data)
        except (EntityNotFoundException, ValidationException) as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], permission_classes=[IsAdminRole])
    def decrementar(self, request, pk=None):
        """POST /api/inventario/{id}/decrementar/ - Decrementar stock"""
        cantidad = request.data.get('cantidad', 0)
        try:
            inventario = self._use_cases.decrementar_stock(int(pk), int(cantidad))
            output_serializer = InventarioOutputSerializer(inventario.to_dict())
            return Response(output_serializer.data)
        except EntityNotFoundException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_404_NOT_FOUND
            )
        except BusinessRuleViolationException as e:
            return Response(
                {'error': e.message},
                status=status.HTTP_400_BAD_REQUEST
            )


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
