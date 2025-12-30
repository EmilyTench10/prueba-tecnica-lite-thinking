"""
Entidad de Dominio: Empresa

Este modelo representa una empresa en el sistema.
Utiliza el NIT como llave primaria para garantizar unicidad.

NOTA: Este es el modelo canónico del dominio. Las apps del backend
deben importar desde aquí usando: from domain.models import Empresa
"""
from django.db import models
from django.core.exceptions import ValidationError


class Empresa(models.Model):
    """
    Modelo para empresas.

    Atributos:
        nit: Identificador único (NIT) - Llave primaria
        nombre: Nombre de la empresa
        direccion: Dirección física
        telefono: Número de teléfono de contacto
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    nit = models.CharField(
        'NIT',
        max_length=20,
        primary_key=True,
        help_text='Número de Identificación Tributaria'
    )
    nombre = models.CharField('Nombre de la empresa', max_length=200)
    direccion = models.CharField('Dirección', max_length=300)
    telefono = models.CharField('Teléfono', max_length=20)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        # Usar el app_label original para mantener compatibilidad con migraciones
        app_label = 'empresas'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.nit})"

    def clean(self):
        """Validaciones de reglas de negocio"""
        if not self.nombre or not self.nombre.strip():
            raise ValidationError({'nombre': 'El nombre de la empresa no puede estar vacío'})

        if not self.direccion or not self.direccion.strip():
            raise ValidationError({'direccion': 'La dirección no puede estar vacía'})

        if not self.telefono or not self.telefono.strip():
            raise ValidationError({'telefono': 'El teléfono no puede estar vacío'})

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip() if self.nombre else ''
        self.direccion = self.direccion.strip() if self.direccion else ''
        self.telefono = self.telefono.strip() if self.telefono else ''
        self.full_clean()
        super().save(*args, **kwargs)
