"""
Entidad de Dominio: Inventario

Este modelo representa el inventario de productos por empresa.

NOTA: Este es el modelo canónico del dominio. Las apps del backend
deben importar desde aquí usando: from domain.models import Inventario
"""
from django.db import models
from django.core.exceptions import ValidationError


class Inventario(models.Model):
    """
    Modelo para inventario de productos por empresa.

    Regla de negocio: Único registro por combinación empresa-producto.

    Atributos:
        empresa: Empresa propietaria (FK)
        producto: Producto en inventario (FK)
        cantidad: Cantidad disponible
        ubicacion: Ubicación física del inventario
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name='Empresa'
    )
    producto = models.ForeignKey(
        'productos.Producto',
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name='Producto'
    )
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    ubicacion = models.CharField('Ubicación', max_length=100, blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        # Usar el app_label original para mantener compatibilidad con migraciones
        app_label = 'inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ['empresa', 'producto']
        ordering = ['empresa', 'producto']

    def __str__(self):
        return f"{self.empresa.nombre} - {self.producto.nombre}: {self.cantidad}"

    def clean(self):
        """Validaciones de reglas de negocio"""
        if self.cantidad < 0:
            raise ValidationError({'cantidad': 'La cantidad no puede ser negativa'})

    def save(self, *args, **kwargs):
        self.ubicacion = self.ubicacion.strip() if self.ubicacion else ''
        self.full_clean()
        super().save(*args, **kwargs)

    def agregar_stock(self, cantidad: int) -> None:
        """Agrega stock al inventario"""
        if cantidad < 0:
            raise ValidationError({'cantidad': 'La cantidad a agregar no puede ser negativa'})
        self.cantidad += cantidad
        self.save()

    def remover_stock(self, cantidad: int) -> None:
        """Remueve stock del inventario"""
        if cantidad < 0:
            raise ValidationError({'cantidad': 'La cantidad a remover no puede ser negativa'})
        if cantidad > self.cantidad:
            raise ValidationError({'cantidad': 'No hay suficiente stock disponible'})
        self.cantidad -= cantidad
        self.save()
