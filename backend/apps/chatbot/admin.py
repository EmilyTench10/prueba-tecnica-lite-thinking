from django.contrib import admin
from .models import ConversacionChat, MensajeChat


class MensajeChatInline(admin.TabularInline):
    model = MensajeChat
    extra = 0
    readonly_fields = ['tipo', 'mensaje', 'timestamp']


@admin.register(ConversacionChat)
class ConversacionChatAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'usuario', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_id', 'usuario__email']
    inlines = [MensajeChatInline]


@admin.register(MensajeChat)
class MensajeChatAdmin(admin.ModelAdmin):
    list_display = ['conversacion', 'tipo', 'mensaje_corto', 'timestamp']
    list_filter = ['tipo', 'timestamp']

    def mensaje_corto(self, obj):
        return f"{obj.mensaje[:50]}..." if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'
