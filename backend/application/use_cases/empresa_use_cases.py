"""
Casos de Uso: Empresa

Orquesta las operaciones CRUD de empresas.
Trabaja directamente con los modelos Django del dominio.
"""
from typing import List, Optional
from dataclasses import dataclass
from django.db.models import Q

from domain.models import Empresa
from domain.exceptions import (
    EntityNotFoundException,
    DuplicateEntityException,
    ValidationException
)


@dataclass
class EmpresaDTO:
    """Data Transfer Object para Empresa"""
    nit: str
    nombre: str
    direccion: str
    telefono: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_model(cls, empresa: Empresa) -> 'EmpresaDTO':
        """Crea un DTO desde un modelo Django"""
        return cls(
            nit=empresa.nit,
            nombre=empresa.nombre,
            direccion=empresa.direccion,
            telefono=empresa.telefono,
            created_at=empresa.created_at.isoformat() if empresa.created_at else None,
            updated_at=empresa.updated_at.isoformat() if empresa.updated_at else None,
        )

    def to_dict(self) -> dict:
        return {
            'nit': self.nit,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


class EmpresaUseCases:
    """
    Casos de uso para operaciones de Empresa.
    Trabaja directamente con el modelo Empresa del dominio.
    """

    def crear_empresa(
        self,
        nit: str,
        nombre: str,
        direccion: str,
        telefono: str
    ) -> EmpresaDTO:
        """Crea una nueva empresa"""
        if Empresa.objects.filter(nit=nit).exists():
            raise DuplicateEntityException('Empresa', nit)

        try:
            empresa = Empresa.objects.create(
                nit=nit,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono
            )
            return EmpresaDTO.from_model(empresa)
        except Exception as e:
            raise ValidationException(str(e))

    def actualizar_empresa(
        self,
        nit: str,
        nombre: Optional[str] = None,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None
    ) -> EmpresaDTO:
        """Actualiza una empresa existente"""
        try:
            empresa = Empresa.objects.get(nit=nit)
        except Empresa.DoesNotExist:
            raise EntityNotFoundException('Empresa', nit)

        if nombre is not None:
            empresa.nombre = nombre
        if direccion is not None:
            empresa.direccion = direccion
        if telefono is not None:
            empresa.telefono = telefono

        empresa.save()
        return EmpresaDTO.from_model(empresa)

    def obtener_empresa(self, nit: str) -> EmpresaDTO:
        """Obtiene una empresa por NIT"""
        try:
            empresa = Empresa.objects.get(nit=nit)
            return EmpresaDTO.from_model(empresa)
        except Empresa.DoesNotExist:
            raise EntityNotFoundException('Empresa', nit)

    def listar_empresas(self) -> List[EmpresaDTO]:
        """Lista todas las empresas"""
        empresas = Empresa.objects.all()
        return [EmpresaDTO.from_model(e) for e in empresas]

    def buscar_empresas(self, termino: str) -> List[EmpresaDTO]:
        """Busca empresas por término"""
        empresas = Empresa.objects.filter(
            Q(nit__icontains=termino) |
            Q(nombre__icontains=termino)
        )
        return [EmpresaDTO.from_model(e) for e in empresas]

    def eliminar_empresa(self, nit: str) -> bool:
        """Elimina una empresa"""
        try:
            empresa = Empresa.objects.get(nit=nit)
            empresa.delete()
            return True
        except Empresa.DoesNotExist:
            raise EntityNotFoundException('Empresa', nit)

    def contar_empresas(self) -> int:
        """Cuenta el total de empresas"""
        return Empresa.objects.count()
