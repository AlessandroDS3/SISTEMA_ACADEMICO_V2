"""Interfaz de repositorio del dominio (UMLInterface IRespuestaEstudianteRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante


class IRespuestaEstudianteRepositorio(ABC):

    @abstractmethod
    def guardar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[RespuestaEstudiante]:
        ...

    @abstractmethod
    def buscar_por_examen(self, examen_id: int) -> List[RespuestaEstudiante]:
        ...

    @abstractmethod
    def buscar_por_estudiante(self, estudiante_id: int) -> List[RespuestaEstudiante]:
        ...

    @abstractmethod
    def actualizar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[RespuestaEstudiante]:
        ...
