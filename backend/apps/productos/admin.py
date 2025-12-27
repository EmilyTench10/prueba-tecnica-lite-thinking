from django.contrib import admin
from .models import Producto, PrecioProducto


class PrecioProductoInline(admin.TabularInline):
    model = PrecioProducto
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'empresa', 'created_at']
    search_fields = ['codigo', 'nombre', 'empresa__nombre']
    list_filter = ['empresa', 'created_at']
    ordering = ['nombre']
    inlines = [PrecioProductoInline]


@admin.register(PrecioProducto)
class PrecioProductoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'moneda', 'precio']
    list_filter = ['moneda']
    search_fields = ['producto__nombre']
