"""
Casos de Uso: Inventario

Orquesta las operaciones CRUD de inventario.
Trabaja directamente con los modelos Django del dominio.
"""
from typing import List, Optional
from dataclasses import dataclass
from django.db.models import Sum

from domain.models import Inventario, Empresa, Producto
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException,
    BusinessRuleViolationException
)


@dataclass
class InventarioDTO:
    """Data Transfer Object para Inventario"""
    empresa: str
    producto: str
    cantidad: int
    ubicacion: str
    empresa_nombre: str = ""
    producto_nombre: str = ""
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_model(cls, inv: Inventario) -> 'InventarioDTO':
        return cls(
            id=inv.id,
            empresa=inv.empresa_id,
            empresa_nombre=inv.empresa.nombre if inv.empresa else "",
            producto=inv.producto.codigo if inv.producto else "",
            producto_nombre=inv.producto.nombre if inv.producto else "",
            cantidad=inv.cantidad,
            ubicacion=inv.ubicacion,
            created_at=inv.created_at.isoformat() if inv.created_at else None,
            updated_at=inv.updated_at.isoformat() if inv.updated_at else None,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'empresa': self.empresa,
            'empresa_nombre': self.empresa_nombre,
            'producto': self.producto,
            'producto_nombre': self.producto_nombre,
            'cantidad': self.cantidad,
            'ubicacion': self.ubicacion,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class InventarioUseCases:
    """
    Casos de uso para operaciones de Inventario.
    Trabaja directamente con los modelos del dominio.
    """

    def crear_registro(
        self,
        empresa_nit: str,
        producto_codigo: str,
        cantidad: int,
        ubicacion: str = ""
    ) -> InventarioDTO:
        """Crea un nuevo registro de inventario"""
        # Verificar empresa
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
        except Empresa.DoesNotExist:
            raise EntityNotFoundException('Empresa', empresa_nit)

        # Verificar producto
        try:
            producto = Producto.objects.get(codigo=producto_codigo)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', producto_codigo)

        # Verificar duplicado
        if Inventario.objects.filter(empresa=empresa, producto=producto).exists():
            raise DuplicateEntityException(
                'Inventario',
                f'{empresa_nit}-{producto_codigo}'
            )

        try:
            inventario = Inventario.objects.create(
                empresa=empresa,
                producto=producto,
                cantidad=cantidad,
                ubicacion=ubicacion or ""
            )
            return InventarioDTO.from_model(inventario)
        except Exception as e:
            raise ValidationException(str(e))

    def actualizar_registro(
        self,
        id: int,
        cantidad: Optional[int] = None,
        ubicacion: Optional[str] = None
    ) -> InventarioDTO:
        """Actualiza un registro de inventario"""
        try:
            inventario = Inventario.objects.select_related('empresa', 'producto').get(id=id)
        except Inventario.DoesNotExist:
            raise EntityNotFoundException('Inventario', id)

        if cantidad is not None:
            inventario.cantidad = cantidad
        if ubicacion is not None:
            inventario.ubicacion = ubicacion

        inventario.save()
        return InventarioDTO.from_model(inventario)

    def incrementar_stock(self, id: int, cantidad: int) -> InventarioDTO:
        """Incrementa el stock"""
        try:
            inventario = Inventario.objects.select_related('empresa', 'producto').get(id=id)
        except Inventario.DoesNotExist:
            raise EntityNotFoundException('Inventario', id)

        if cantidad < 0:
            raise ValidationException("La cantidad a incrementar no puede ser negativa")

        inventario.cantidad += cantidad
        inventario.save()
        return InventarioDTO.from_model(inventario)

    def decrementar_stock(self, id: int, cantidad: int) -> InventarioDTO:
        """Decrementa el stock"""
        try:
            inventario = Inventario.objects.select_related('empresa', 'producto').get(id=id)
        except Inventario.DoesNotExist:
            raise EntityNotFoundException('Inventario', id)

        if cantidad < 0:
            raise ValidationException("La cantidad a decrementar no puede ser negativa")

        if cantidad > inventario.cantidad:
            raise BusinessRuleViolationException(
                "stock_insuficiente",
                f"Stock insuficiente. Disponible: {inventario.cantidad}, Solicitado: {cantidad}"
            )

        inventario.cantidad -= cantidad
        inventario.save()
        return InventarioDTO.from_model(inventario)

    def obtener_registro(self, id: int) -> InventarioDTO:
        """Obtiene un registro por ID"""
        try:
            inventario = Inventario.objects.select_related('empresa', 'producto').get(id=id)
            return InventarioDTO.from_model(inventario)
        except Inventario.DoesNotExist:
            raise EntityNotFoundException('Inventario', id)

    def listar_inventario(self) -> List[InventarioDTO]:
        """Lista todo el inventario"""
        inventarios = Inventario.objects.select_related('empresa', 'producto').all()
        return [InventarioDTO.from_model(i) for i in inventarios]

    def listar_por_empresa(self, empresa_nit: str) -> List[InventarioDTO]:
        """Lista inventario de una empresa"""
        inventarios = Inventario.objects.select_related('empresa', 'producto').filter(
            empresa_id=empresa_nit
        )
        return [InventarioDTO.from_model(i) for i in inventarios]

    def listar_con_stock(self) -> List[InventarioDTO]:
        """Lista registros con stock disponible"""
        inventarios = Inventario.objects.select_related('empresa', 'producto').filter(
            cantidad__gt=0
        )
        return [InventarioDTO.from_model(i) for i in inventarios]

    def listar_sin_stock(self) -> List[InventarioDTO]:
        """Lista registros sin stock"""
        inventarios = Inventario.objects.select_related('empresa', 'producto').filter(
            cantidad=0
        )
        return [InventarioDTO.from_model(i) for i in inventarios]

    def eliminar_registro(self, id: int) -> bool:
        """Elimina un registro"""
        try:
            inventario = Inventario.objects.get(id=id)
            inventario.delete()
            return True
        except Inventario.DoesNotExist:
            raise EntityNotFoundException('Inventario', id)

    def verificar_disponibilidad(
        self,
        empresa_nit: str,
        producto_codigo: str,
        cantidad: int
    ) -> bool:
        """Verifica si hay stock suficiente"""
        try:
            inventario = Inventario.objects.get(
                empresa_id=empresa_nit,
                producto__codigo=producto_codigo
            )
            return inventario.cantidad >= cantidad
        except Inventario.DoesNotExist:
            return False

    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas de inventario"""
        total_registros = Inventario.objects.count()
        total_unidades = Inventario.objects.aggregate(
            total=Sum('cantidad')
        )['total'] or 0
        con_stock = Inventario.objects.filter(cantidad__gt=0).count()
        sin_stock = Inventario.objects.filter(cantidad=0).count()

        return {
            'total_registros': total_registros,
            'total_unidades': total_unidades,
            'registros_con_stock': con_stock,
            'registros_sin_stock': sin_stock,
        }
