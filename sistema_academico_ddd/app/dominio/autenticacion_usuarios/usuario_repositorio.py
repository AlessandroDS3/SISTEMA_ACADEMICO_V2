"""Interfaz de repositorio del dominio (UMLInterface IUsuarioRepositorio).

La implementacion concreta vive en la capa de infraestructura
(`app.infraestructura.repositorios.usuario_repositorio_impl`), acorde
al patron Repository de DDD: el dominio depende de la abstraccion,
no de SQLAlchemy directamente.
"""
from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional

from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum


class IUsuarioRepositorio(ABC):

    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        ...

    @abstractmethod
    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[Usuario]:
        ...

    @abstractmethod
    def contar_por_rol(self) -> Dict[RolEnum, int]:
        """Estilo Persistent-Tables: un conteo agregado por rol."""
        ...

    @abstractmethod
    def iterar_todos(self) -> Iterator[Usuario]:
        """Estilo Lazy-Rivers: recorre la tabla de forma perezosa."""
        ...
