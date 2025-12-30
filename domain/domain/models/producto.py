"""
Entidades de Dominio: Producto y PrecioProducto

Estos modelos representan productos y sus precios en múltiples monedas.

NOTA: Estos son los modelos canónicos del dominio. Las apps del backend
deben importar desde aquí usando: from domain.models import Producto, PrecioProducto
"""
from django.db import models
from django.core.exceptions import ValidationError


class Producto(models.Model):
    """
    Modelo para productos.

    Atributos:
        codigo: Código único del producto
        nombre: Nombre del producto
        caracteristicas: Descripción de características
        empresa: Empresa propietaria (FK)
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    codigo = models.CharField('Código', max_length=50, unique=True)
    nombre = models.CharField('Nombre del producto', max_length=200)
    caracteristicas = models.TextField('Características', blank=True)
    empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name='Empresa'
    )
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)

    class Meta:
        # Usar el app_label original para mantener compatibilidad con migraciones
        app_label = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    def clean(self):
        """Validaciones de reglas de negocio"""
        if not self.nombre or not self.nombre.strip():
            raise ValidationError({'nombre': 'El nombre del producto no puede estar vacío'})

        if not self.codigo or not self.codigo.strip():
            raise ValidationError({'codigo': 'El código del producto no puede estar vacío'})

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.strip() if self.nombre else ''
        self.codigo = self.codigo.strip() if self.codigo else ''
        self.caracteristicas = self.caracteristicas.strip() if self.caracteristicas else ''
        self.full_clean()
        super().save(*args, **kwargs)


class PrecioProducto(models.Model):
    """
    Modelo para precios en múltiples monedas.

    Regla de negocio: Solo puede haber un precio por producto por moneda.
    """

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
        # Usar el app_label original para mantener compatibilidad con migraciones
        app_label = 'productos'
        verbose_name = 'Precio de Producto'
        verbose_name_plural = 'Precios de Productos'
        unique_together = ['producto', 'moneda']

    def __str__(self):
        return f"{self.producto.nombre} - {self.precio} {self.moneda}"

    def clean(self):
        """Validaciones de reglas de negocio"""
        if self.precio is not None and self.precio < 0:
            raise ValidationError({'precio': 'El precio no puede ser negativo'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
