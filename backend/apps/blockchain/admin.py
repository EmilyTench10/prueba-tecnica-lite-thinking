from django.contrib import admin
from .models import RegistroBlockchain


@admin.register(RegistroBlockchain)
class RegistroBlockchainAdmin(admin.ModelAdmin):
    list_display = ['indice', 'tipo', 'usuario', 'timestamp', 'hash_actual_corto']
    list_filter = ['tipo', 'timestamp']
    search_fields = ['usuario', 'hash_actual']
    readonly_fields = ['indice', 'hash_anterior', 'hash_actual', 'timestamp']
    ordering = ['-indice']

    def hash_actual_corto(self, obj):
        return f"{obj.hash_actual[:16]}..."
    hash_actual_corto.short_description = 'Hash'
