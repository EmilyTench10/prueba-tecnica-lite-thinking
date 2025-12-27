from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventarioViewSet, DescargarPDFView, EnviarPDFEmailView

router = DefaultRouter()
router.register('inventario', InventarioViewSet, basename='inventario')

urlpatterns = [
    # Rutas personalizadas ANTES del router
    path('inventario/descargar-pdf/', DescargarPDFView.as_view(), name='descargar-pdf'),
    path('inventario/enviar-pdf/', EnviarPDFEmailView.as_view(), name='enviar-pdf'),
    path('', include(router.urls)),
]
