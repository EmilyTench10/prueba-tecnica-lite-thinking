from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.empresas.models import Empresa
from apps.productos.models import Producto, PrecioProducto
from apps.inventario.models import Inventario
from apps.users.models import User
from apps.blockchain.models import RegistroBlockchain
from apps.blockchain.middleware import get_current_user


def get_username():
    """Obtiene el email del usuario actual o 'sistema' si no hay usuario"""
    user = get_current_user()
    if user and user.is_authenticated:
        return user.email
    return 'sistema'


# Signals para Empresa
@receiver(post_save, sender=Empresa)
def registrar_empresa(sender, instance, created, **kwargs):
    """Registra creación o modificación de empresa en blockchain"""
    tipo = 'empresa_creada' if created else 'empresa_modificada'
    datos = {
        'nit': instance.nit,
        'nombre': instance.nombre,
        'direccion': instance.direccion,
        'telefono': instance.telefono,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo=tipo,
        datos=datos,
        usuario=get_username()
    )


# Signals para Producto
@receiver(post_save, sender=Producto)
def registrar_producto(sender, instance, created, **kwargs):
    """Registra creación o modificación de producto en blockchain"""
    tipo = 'producto_creado' if created else 'producto_modificado'
    datos = {
        'id': instance.id,
        'codigo': instance.codigo,
        'nombre': instance.nombre,
        'empresa': instance.empresa.nit if instance.empresa else None,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo=tipo,
        datos=datos,
        usuario=get_username()
    )


# Signals para Inventario
@receiver(post_save, sender=Inventario)
def registrar_inventario(sender, instance, created, **kwargs):
    """Registra actualización de inventario en blockchain"""
    datos = {
        'id': instance.id,
        'empresa': instance.empresa.nit if instance.empresa else None,
        'producto': instance.producto.nombre if instance.producto else None,
        'cantidad': instance.cantidad,
        'ubicacion': instance.ubicacion,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo='inventario_actualizado',
        datos=datos,
        usuario=get_username()
    )


# Signals para Usuario
@receiver(post_save, sender=User)
def registrar_usuario(sender, instance, created, **kwargs):
    """Registra creación de usuario en blockchain"""
    if created:
        datos = {
            'email': instance.email,
            'role': instance.role,
        }
        RegistroBlockchain.registrar_transaccion(
            tipo='usuario_creado',
            datos=datos,
            usuario=get_username()
        )


# Signals para eliminaciones
@receiver(post_delete, sender=Empresa)
def registrar_empresa_eliminada(sender, instance, **kwargs):
    """Registra eliminación de empresa en blockchain"""
    datos = {
        'nit': instance.nit,
        'nombre': instance.nombre,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo='empresa_eliminada',
        datos=datos,
        usuario=get_username()
    )


@receiver(post_delete, sender=Producto)
def registrar_producto_eliminado(sender, instance, **kwargs):
    """Registra eliminación de producto en blockchain"""
    datos = {
        'id': instance.id,
        'codigo': instance.codigo,
        'nombre': instance.nombre,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo='producto_eliminado',
        datos=datos,
        usuario=get_username()
    )


@receiver(post_delete, sender=Inventario)
def registrar_inventario_eliminado(sender, instance, **kwargs):
    """Registra eliminación de item de inventario en blockchain"""
    datos = {
        'id': instance.id,
        'empresa': instance.empresa.nit if instance.empresa else None,
        'producto': instance.producto.nombre if instance.producto else None,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo='inventario_eliminado',
        datos=datos,
        usuario=get_username()
    )


@receiver(post_delete, sender=User)
def registrar_usuario_eliminado(sender, instance, **kwargs):
    """Registra eliminación de usuario en blockchain"""
    datos = {
        'email': instance.email,
        'role': instance.role,
    }
    RegistroBlockchain.registrar_transaccion(
        tipo='usuario_eliminado',
        datos=datos,
        usuario=get_username()
    )
