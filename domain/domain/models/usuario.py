"""
Entidad de Dominio: Usuario

Este modelo representa un usuario del sistema con roles.
Extiende AbstractUser de Django para autenticación.

NOTA: Este es el modelo canónico del dominio. Las apps del backend
deben importar desde aquí usando: from domain.models import User
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """Manager personalizado para User con email en lugar de username"""

    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular"""
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuario personalizado con roles.

    Usa email como identificador único en lugar de username.

    Roles:
        admin: Acceso completo al sistema
        externo: Acceso limitado (solo lectura de catálogo)
    """

    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('externo', 'Externo'),
    ]

    username = None
    email = models.EmailField('Correo electrónico', unique=True)
    role = models.CharField(
        'Rol',
        max_length=20,
        choices=ROLE_CHOICES,
        default='externo'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        # Usar el app_label original para mantener compatibilidad con migraciones
        app_label = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['email']

    def __str__(self):
        return self.email

    def clean(self):
        """Validaciones de reglas de negocio"""
        if not self.email or not self.email.strip():
            raise ValidationError({'email': 'El email es obligatorio'})

    @property
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == 'admin' or self.is_superuser

    @property
    def is_externo(self):
        """Verifica si el usuario es externo"""
        return self.role == 'externo'
