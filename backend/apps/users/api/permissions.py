from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Permiso para usuarios con rol administrador"""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsExternoRole(BasePermission):
    """Permiso para usuarios con rol externo"""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'externo'
        )


class IsAdminOrReadOnly(BasePermission):
    """Admin puede todo, otros solo lectura"""

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )
