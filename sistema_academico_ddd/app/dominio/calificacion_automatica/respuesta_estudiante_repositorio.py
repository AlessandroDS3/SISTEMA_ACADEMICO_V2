"""Interfaz de repositorio del dominio (UMLInterface IRespuestaEstudianteRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante


class IRespuestaEstudianteRepositorio(ABC):
    """Estilo Persistent-Tables: ademas de los metodos CRUD, expone
    consultas agregadas (`promedio_nota_por_examen`,
    `contar_por_umbral_nota`) para que sea la base de datos quien haga
    el AVG/COUNT, en vez de traer todas las filas a Python y calcular
    el agregado ahi con un `for`."""

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

    @abstractmethod
    def promedio_nota_por_examen(self, examen_id: int) -> float:
        ...

    @abstractmethod
    def contar_por_umbral_nota(self, examen_id: int, nota_minima_aprobatoria: float) -> Tuple[int, int]:
        ...
