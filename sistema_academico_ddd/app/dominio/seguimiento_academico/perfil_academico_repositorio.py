"""Interfaces de repositorio del dominio para PerfilAcademico.

Principio de Segregacion de Interfaces (ISP): antes existia un unico
contrato de 6 metodos (CRUD completo) que `PerfilAcademicoAppService`
debia declarar como dependencia aunque solo invocara 3 de ellos
(`guardar`, `buscar_por_estudiante`, `listar`). Ningun caso de uso del
subdominio llama a `buscar_por_id`, `actualizar` ni `eliminar`.

Se separan en dos interfaces mas pequeñas: `IPerfilAcademicoRepositorio`
conserva solo lo que el caso de uso real consume, e
`IPerfilAcademicoMantenimiento` agrupa las operaciones administrativas
que hoy nadie necesita, para no forzar a los clientes futuros a
depender de metodos que no usan.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico


class IPerfilAcademicoRepositorio(ABC):
    """Operaciones que consume el caso de uso de seguimiento academico."""

    @abstractmethod
    def guardar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        ...

    @abstractmethod
    def buscar_por_estudiante(self, estudiante_id: int) -> Optional[PerfilAcademico]:
        ...

    @abstractmethod
    def listar(self) -> List[PerfilAcademico]:
        ...


class IPerfilAcademicoMantenimiento(ABC):
    """Operaciones administrativas que ningun caso de uso actual invoca."""

    @abstractmethod
    def buscar_por_id(self, perfil_id: int) -> Optional[PerfilAcademico]:
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
