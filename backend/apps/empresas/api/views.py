from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.empresas.models import Empresa
from apps.users.api.permissions import IsAdminOrReadOnly
from .serializers import EmpresaSerializer, EmpresaListSerializer


class EmpresaViewSet(ModelViewSet):
    """
    ViewSet para CRUD de empresas
    - Admin: puede crear, editar, eliminar
    - Externo: solo puede ver (lectura)
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'nit'

    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        return EmpresaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminOrReadOnly()]
