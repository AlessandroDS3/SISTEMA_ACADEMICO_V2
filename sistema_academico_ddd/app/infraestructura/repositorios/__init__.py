"""Implementaciones concretas de los repositorios del dominio (SQLAlchemy)."""
from app.infraestructura.repositorios.usuario_repositorio_impl import UsuarioRepositorioImpl
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl
from app.infraestructura.repositorios.respuesta_estudiante_repositorio_impl import (
    RespuestaEstudianteRepositorioImpl,
)
from app.infraestructura.repositorios.perfil_academico_repositorio_impl import (
    PerfilAcademicoRepositorioImpl,
)
from app.infraestructura.repositorios.reporte_institucional_repositorio_impl import (
    ReporteInstitucionalRepositorioImpl,
)

__all__ = [
    "UsuarioRepositorioImpl",
    "ExamenRepositorioImpl",
    "RespuestaEstudianteRepositorioImpl",
    "PerfilAcademicoRepositorioImpl",
    "ReporteInstitucionalRepositorioImpl",
]
