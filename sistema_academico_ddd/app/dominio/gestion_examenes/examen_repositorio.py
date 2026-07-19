"""Interfaz de repositorio del dominio (UMLInterface IExamenRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.gestion_examenes.examen import Examen


class IExamenRepositorio(ABC):

    @abstractmethod
    def guardar(self, examen: Examen) -> Examen:
        ...

    @abstractmethod
    def buscar_por_id(self, examen_id: int) -> Optional[Examen]:
        ...

    @abstractmethod
    def buscar_por_materia(self, materia_id: int) -> List[Examen]:
        ...

    @abstractmethod
    def actualizar(self, examen: Examen) -> Examen:
        ...

    @abstractmethod
    def eliminar(self, examen_id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[Examen]:
        ...

    @abstractmethod
    def contar_preguntas_por_examen(self, examen_id: int) -> int:
        """Estilo Persistent-Tables: conteo agregado en la base de
        datos en vez de `len(examen.preguntas)` sobre la coleccion ya
        cargada en memoria."""
        ...
