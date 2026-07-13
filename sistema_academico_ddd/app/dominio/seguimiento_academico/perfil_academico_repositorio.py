"""Interfaz de repositorio del dominio (UMLInterface IPerfilAcademicoRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico


class IPerfilAcademicoRepositorio(ABC):

    @abstractmethod
    def guardar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[PerfilAcademico]:
        ...

    @abstractmethod
    def buscar_por_estudiante(self, estudiante_id: int) -> Optional[PerfilAcademico]:
        ...

    @abstractmethod
    def actualizar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[PerfilAcademico]:
        ...
