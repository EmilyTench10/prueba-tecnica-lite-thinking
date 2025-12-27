from django.db import models
from django.utils import timezone
import hashlib
import json


class RegistroBlockchain(models.Model):
    """
    Modelo para registrar transacciones en una cadena de bloques simplificada
    Implementa verificación de integridad mediante hash encadenado
    """

    TIPO_CHOICES = [
        ('empresa_creada', 'Empresa Creada'),
        ('empresa_modificada', 'Empresa Modificada'),
        ('empresa_eliminada', 'Empresa Eliminada'),
        ('producto_creado', 'Producto Creado'),
        ('producto_modificado', 'Producto Modificado'),
        ('producto_eliminado', 'Producto Eliminado'),
        ('inventario_actualizado', 'Inventario Actualizado'),
        ('inventario_eliminado', 'Inventario Eliminado'),
        ('usuario_creado', 'Usuario Creado'),
        ('usuario_eliminado', 'Usuario Eliminado'),
    ]

    indice = models.AutoField(primary_key=True)
    tipo = models.CharField('Tipo de transacción', max_length=50, choices=TIPO_CHOICES)
    datos = models.JSONField('Datos de la transacción')
    timestamp = models.DateTimeField('Marca de tiempo')  # Sin auto_now_add
    hash_anterior = models.CharField('Hash anterior', max_length=64, blank=True)
    hash_actual = models.CharField('Hash actual', max_length=64)
    usuario = models.CharField('Usuario', max_length=100)

    class Meta:
        verbose_name = 'Registro Blockchain'
        verbose_name_plural = 'Registros Blockchain'
        ordering = ['-indice']

    def __str__(self):
        return f"Bloque #{self.indice} - {self.tipo}"

    @staticmethod
    def calcular_hash(tipo, datos, timestamp, hash_anterior):
        """Calcula el hash SHA-256 del bloque"""
        contenido = f"{tipo}{json.dumps(datos, sort_keys=True)}{timestamp}{hash_anterior}"
        return hashlib.sha256(contenido.encode()).hexdigest()

    def save(self, *args, **kwargs):
        if not self.hash_actual:
            # Asignar timestamp ANTES de calcular el hash
            if not self.timestamp:
                self.timestamp = timezone.now()

            # Obtener el último bloque
            ultimo_bloque = RegistroBlockchain.objects.order_by('-indice').first()

            if ultimo_bloque:
                self.hash_anterior = ultimo_bloque.hash_actual
            else:
                self.hash_anterior = "0" * 64  # Genesis block

            # Calcular hash con el mismo timestamp que se guardará
            self.hash_actual = self.calcular_hash(
                self.tipo,
                self.datos,
                self.timestamp.isoformat(),
                self.hash_anterior
            )

        super().save(*args, **kwargs)

    @classmethod
    def verificar_integridad(cls):
        """Verifica la integridad de toda la cadena"""
        bloques = cls.objects.order_by('indice')
        errores = []

        hash_anterior = "0" * 64

        for bloque in bloques:
            # Verificar enlace con bloque anterior
            if bloque.hash_anterior != hash_anterior:
                errores.append({
                    'bloque': bloque.indice,
                    'error': 'Hash anterior no coincide',
                    'esperado': hash_anterior,
                    'encontrado': bloque.hash_anterior
                })

            # Verificar hash actual
            hash_calculado = cls.calcular_hash(
                bloque.tipo,
                bloque.datos,
                bloque.timestamp.isoformat(),
                bloque.hash_anterior
            )

            if bloque.hash_actual != hash_calculado:
                errores.append({
                    'bloque': bloque.indice,
                    'error': 'Hash actual no coincide (posible manipulación)',
                    'esperado': hash_calculado,
                    'encontrado': bloque.hash_actual
                })

            hash_anterior = bloque.hash_actual

        return {
            'valido': len(errores) == 0,
            'total_bloques': bloques.count(),
            'errores': errores
        }

    @classmethod
    def registrar_transaccion(cls, tipo, datos, usuario):
        """Registra una nueva transacción en la blockchain"""
        registro = cls(
            tipo=tipo,
            datos=datos,
            usuario=usuario
        )
        registro.save()
        return registro
