"""Interfaz de repositorio del dominio (UMLInterface IReporteInstitucionalRepositorio)."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional


class IReporteInstitucionalRepositorio(ABC):

    @abstractmethod
    def guardar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        ...

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[ReporteInstitucional]:
        ...

    @abstractmethod
    def buscar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        ...

    @abstractmethod
    def actualizar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        ...

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        ...

    @abstractmethod
    def listar(self) -> List[ReporteInstitucional]:
        ...
