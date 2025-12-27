from django.db import models


class Empresa(models.Model):
    """Modelo para empresas - NIT como llave primaria"""

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
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.nit})"
