"""
URL configuration for Lite Thinking project
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Lite Thinking API",
        default_version='v1',
        description="API para gestión de empresas, productos e inventario",
        contact=openapi.Contact(email="admin@litethinking.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('apps.users.api.router')),
    path('api/', include('apps.empresas.api.router')),
    path('api/', include('apps.productos.api.router')),
    path('api/', include('apps.inventario.api.router')),
    path('api/', include('apps.blockchain.api.router')),
    path('api/', include('apps.chatbot.api.router')),

    # Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
