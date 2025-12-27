from django.contrib import admin
from .models import Inventario


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'producto', 'cantidad', 'ubicacion', 'updated_at']
    search_fields = ['empresa__nombre', 'producto__nombre']
    list_filter = ['empresa', 'updated_at']
    ordering = ['empresa', 'producto']
