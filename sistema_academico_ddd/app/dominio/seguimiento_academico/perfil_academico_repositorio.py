"""Interfaz de repositorio del dominio (UMLInterface IPerfilAcademicoRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico


class IPerfilAcademicoRepositorio(ABC):

    @abstractmethod
    def guardar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        ...

    @abstractmethod
    def buscar_por_id(self, perfil_id: int) -> Optional[PerfilAcademico]:
        ...

    @abstractmethod
    def buscar_por_estudiante(self, estudiante_id: int) -> Optional[PerfilAcademico]:
        ...

    @abstractmethod
    def actualizar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        ...

    @abstractmethod
    def eliminar(self, perfil_id: int) -> None:
        """Elimina el perfil indicado.

        Lanza `PerfilNoEncontradoError` si no existe, en vez de devolver
        un codigo de error booleano.
        """
        ...

    @abstractmethod
    def listar(self) -> List[PerfilAcademico]:
        ...
