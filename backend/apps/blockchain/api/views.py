from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from apps.blockchain.models import RegistroBlockchain
from apps.users.api.permissions import IsAdminRole
from .serializers import RegistroBlockchainSerializer, VerificarIntegridadSerializer


class BlockchainViewSet(ReadOnlyModelViewSet):
    """ViewSet de solo lectura para ver registros blockchain"""
    queryset = RegistroBlockchain.objects.all()
    serializer_class = RegistroBlockchainSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def verificar(self, request):
        """Verificar integridad de la cadena"""
        resultado = RegistroBlockchain.verificar_integridad()
        return Response(resultado)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas de la blockchain"""
        from django.db.models import Count

        stats = RegistroBlockchain.objects.values('tipo').annotate(
            total=Count('indice')
        ).order_by('-total')

        ultimo = RegistroBlockchain.objects.order_by('-indice').first()
        primero = RegistroBlockchain.objects.order_by('indice').first()

        return Response({
            'total_bloques': RegistroBlockchain.objects.count(),
            'por_tipo': list(stats),
            'primer_bloque': primero.timestamp.isoformat() if primero else None,
            'ultimo_bloque': ultimo.timestamp.isoformat() if ultimo else None,
            'integridad': RegistroBlockchain.verificar_integridad()['valido']
        })


class RegistrarTransaccionView(APIView):
    """Vista para registrar transacciones manualmente"""
    permission_classes = [IsAdminRole]

    def post(self, request):
        tipo = request.data.get('tipo')
        datos = request.data.get('datos', {})

        if not tipo:
            return Response(
                {'error': 'Se requiere el campo tipo'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar tipo
        tipos_validos = [choice[0] for choice in RegistroBlockchain.TIPO_CHOICES]
        if tipo not in tipos_validos:
            return Response(
                {'error': f'Tipo inválido. Tipos válidos: {tipos_validos}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        registro = RegistroBlockchain.registrar_transaccion(
            tipo=tipo,
            datos=datos,
            usuario=request.user.email
        )

        serializer = RegistroBlockchainSerializer(registro)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
