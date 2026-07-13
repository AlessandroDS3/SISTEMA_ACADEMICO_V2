"""Interfaz de repositorio del dominio (UMLInterface IUsuarioRepositorio).

La implementacion concreta vive en la capa de infraestructura
(`app.infraestructura.repositorios.usuario_repositorio_impl`), acorde
al patron Repository de DDD: el dominio depende de la abstraccion,
no de SQLAlchemy directamente.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.autenticacion_usuarios.usuario import Usuario


class IUsuarioRepositorio(ABC):

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        ...

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[Usuario]:
        ...
