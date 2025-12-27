from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, MeView, RegisterView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # Auth endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='user_me'),
    path('auth/register/', RegisterView.as_view(), name='user_register'),
    # Users CRUD
    path('', include(router.urls)),
]
