from django.db import models
from apps.empresas.models import Empresa


class Producto(models.Model):
    """Modelo para productos"""

    codigo = models.CharField('Código', max_length=50, unique=True)
    nombre = models.CharField('Nombre del producto', max_length=200)
    caracteristicas = models.TextField('Características', blank=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name='Empresa'
    )
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class PrecioProducto(models.Model):
    """Modelo para precios en múltiples monedas"""

    MONEDA_CHOICES = [
        ('COP', 'Peso Colombiano'),
        ('USD', 'Dólar Estadounidense'),
        ('EUR', 'Euro'),
        ('MXN', 'Peso Mexicano'),
        ('BRL', 'Real Brasileño'),
        ('ARS', 'Peso Argentino'),
        ('GBP', 'Libra Esterlina'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='precios',
        verbose_name='Producto'
    )
    moneda = models.CharField('Moneda', max_length=3, choices=MONEDA_CHOICES)
    precio = models.DecimalField('Precio', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'Precio de Producto'
        verbose_name_plural = 'Precios de Productos'
        unique_together = ['producto', 'moneda']

    def __str__(self):
        return f"{self.producto.nombre} - {self.precio} {self.moneda}"
