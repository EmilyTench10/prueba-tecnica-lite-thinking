"""
Casos de Uso: Producto

Orquesta las operaciones CRUD de productos.
Trabaja directamente con los modelos Django del dominio.
"""
from typing import List, Optional
from dataclasses import dataclass, field
from decimal import Decimal
from django.db.models import Q

from domain.models import Producto, PrecioProducto, Empresa
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException,
    BusinessRuleViolationException
)


@dataclass
class PrecioDTO:
    """Data Transfer Object para Precio"""
    moneda: str
    precio: float
    id: Optional[int] = None

    @classmethod
    def from_model(cls, precio: PrecioProducto) -> 'PrecioDTO':
        return cls(
            id=precio.id,
            moneda=precio.moneda,
            precio=float(precio.precio)
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'moneda': self.moneda,
            'precio': self.precio,
        }


@dataclass
class ProductoDTO:
    """Data Transfer Object para Producto"""
    codigo: str
    nombre: str
    caracteristicas: str
    empresa: str
    empresa_nombre: str = ""
    precios: List[PrecioDTO] = field(default_factory=list)
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_model(cls, producto: Producto) -> 'ProductoDTO':
        return cls(
            id=producto.id,
            codigo=producto.codigo,
            nombre=producto.nombre,
            caracteristicas=producto.caracteristicas,
            empresa=producto.empresa_id,
            empresa_nombre=producto.empresa.nombre if producto.empresa else "",
            precios=[PrecioDTO.from_model(p) for p in producto.precios.all()],
            created_at=producto.created_at.isoformat() if producto.created_at else None,
            updated_at=producto.updated_at.isoformat() if producto.updated_at else None,
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'caracteristicas': self.caracteristicas,
            'empresa': self.empresa,
            'empresa_nombre': self.empresa_nombre,
            'precios': [p.to_dict() for p in self.precios],
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class ProductoUseCases:
    """
    Casos de uso para operaciones de Producto.
    Trabaja directamente con los modelos del dominio.
    """

    def crear_producto(
        self,
        codigo: str,
        nombre: str,
        caracteristicas: str,
        empresa_nit: str,
        precios: Optional[List[dict]] = None
    ) -> ProductoDTO:
        """Crea un nuevo producto"""
        # Verificar que la empresa existe
        try:
            empresa = Empresa.objects.get(nit=empresa_nit)
        except Empresa.DoesNotExist:
            raise EntityNotFoundException('Empresa', empresa_nit)

        # Verificar código único
        if Producto.objects.filter(codigo=codigo).exists():
            raise DuplicateEntityException('Producto', codigo)

        try:
            producto = Producto.objects.create(
                codigo=codigo,
                nombre=nombre,
                caracteristicas=caracteristicas or "",
                empresa=empresa
            )

            # Crear precios si se proporcionan
            if precios:
                for p in precios:
                    PrecioProducto.objects.create(
                        producto=producto,
                        moneda=p['moneda'],
                        precio=Decimal(str(p['precio']))
                    )

            return ProductoDTO.from_model(producto)
        except Exception as e:
            raise ValidationException(str(e))

    def actualizar_producto(
        self,
        id: int,
        nombre: Optional[str] = None,
        caracteristicas: Optional[str] = None
    ) -> ProductoDTO:
        """Actualiza un producto"""
        try:
            producto = Producto.objects.get(id=id)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', id)

        if nombre is not None:
            producto.nombre = nombre
        if caracteristicas is not None:
            producto.caracteristicas = caracteristicas

        producto.save()
        return ProductoDTO.from_model(producto)

    def agregar_precio(
        self,
        producto_id: int,
        monto: float,
        moneda: str
    ) -> ProductoDTO:
        """Agrega o actualiza un precio de un producto"""
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', producto_id)

        # Actualizar si existe, crear si no
        precio, created = PrecioProducto.objects.update_or_create(
            producto=producto,
            moneda=moneda,
            defaults={'precio': Decimal(str(monto))}
        )

        return ProductoDTO.from_model(producto)

    def eliminar_precio(self, producto_id: int, moneda: str) -> ProductoDTO:
        """Elimina un precio de un producto"""
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', producto_id)

        PrecioProducto.objects.filter(producto=producto, moneda=moneda).delete()
        return ProductoDTO.from_model(producto)

    def obtener_producto(self, id: int) -> ProductoDTO:
        """Obtiene un producto por ID"""
        try:
            producto = Producto.objects.select_related('empresa').prefetch_related('precios').get(id=id)
            return ProductoDTO.from_model(producto)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', id)

    def obtener_por_codigo(self, codigo: str) -> ProductoDTO:
        """Obtiene un producto por código"""
        try:
            producto = Producto.objects.select_related('empresa').prefetch_related('precios').get(codigo=codigo)
            return ProductoDTO.from_model(producto)
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', codigo)

    def listar_productos(self) -> List[ProductoDTO]:
        """Lista todos los productos"""
        productos = Producto.objects.select_related('empresa').prefetch_related('precios').all()
        return [ProductoDTO.from_model(p) for p in productos]

    def listar_por_empresa(self, empresa_nit: str) -> List[ProductoDTO]:
        """Lista productos de una empresa"""
        productos = Producto.objects.select_related('empresa').prefetch_related('precios').filter(
            empresa_id=empresa_nit
        )
        return [ProductoDTO.from_model(p) for p in productos]

    def buscar_productos(self, termino: str) -> List[ProductoDTO]:
        """Busca productos por término"""
        productos = Producto.objects.select_related('empresa').prefetch_related('precios').filter(
            Q(codigo__icontains=termino) |
            Q(nombre__icontains=termino)
        )
        return [ProductoDTO.from_model(p) for p in productos]

    def eliminar_producto(self, id: int) -> bool:
        """Elimina un producto"""
        try:
            producto = Producto.objects.get(id=id)
            producto.delete()
            return True
        except Producto.DoesNotExist:
            raise EntityNotFoundException('Producto', id)
