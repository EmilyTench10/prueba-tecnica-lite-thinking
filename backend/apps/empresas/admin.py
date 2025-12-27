from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nit', 'nombre', 'direccion', 'telefono', 'created_at']
    search_fields = ['nit', 'nombre']
    list_filter = ['created_at']
    ordering = ['nombre']
