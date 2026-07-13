"""Subdominio: Reportes y Estadisticas."""
from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional
from app.dominio.reportes_estadisticas.estadistica_grupal import EstadisticaGrupal
from app.dominio.reportes_estadisticas.reporte_institucional_repositorio import (
    IReporteInstitucionalRepositorio,
)

__all__ = [
    "ReporteInstitucional",
    "EstadisticaGrupal",
    "IReporteInstitucionalRepositorio",
]
