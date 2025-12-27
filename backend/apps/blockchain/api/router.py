from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockchainViewSet, RegistrarTransaccionView

router = DefaultRouter()
router.register('blockchain', BlockchainViewSet, basename='blockchain')

urlpatterns = [
    path('', include(router.urls)),
    path('blockchain/registrar/', RegistrarTransaccionView.as_view(), name='registrar-transaccion'),
]
