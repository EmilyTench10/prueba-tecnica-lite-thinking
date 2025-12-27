from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatbotView, ConversacionViewSet, HistorialChatView

router = DefaultRouter()
router.register('conversaciones', ConversacionViewSet, basename='conversaciones')

urlpatterns = [
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
    path('chatbot/historial/<str:session_id>/', HistorialChatView.as_view(), name='historial-chat'),
    path('', include(router.urls)),
]
