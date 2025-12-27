import threading

_user = threading.local()


class CurrentUserMiddleware:
    """
    Middleware para almacenar el usuario actual en una variable thread-local
    Permite acceder al usuario desde cualquier parte del código (signals, models, etc.)
    Soporta autenticación JWT de DRF
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        # Si el usuario es anónimo, intentar autenticación JWT
        if not user or not user.is_authenticated:
            try:
                from rest_framework_simplejwt.authentication import JWTAuthentication
                jwt_auth = JWTAuthentication()
                auth_result = jwt_auth.authenticate(request)
                if auth_result:
                    user = auth_result[0]
            except Exception:
                pass

        _user.value = user
        response = self.get_response(request)
        return response


def get_current_user():
    """Obtiene el usuario actual del request"""
    return getattr(_user, 'value', None)
