from django.db import models
from apps.empresas.models import Empresa
from apps.productos.models import Producto


class Inventario(models.Model):
    """Modelo para inventario de productos por empresa"""

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name='Empresa'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name='Producto'
    )
    cantidad = models.PositiveIntegerField('Cantidad', default=0)
    ubicacion = models.CharField('Ubicación', max_length=100, blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        unique_together = ['empresa', 'producto']
        ordering = ['empresa', 'producto']

    def __str__(self):
        return f"{self.empresa.nombre} - {self.producto.nombre}: {self.cantidad}"
