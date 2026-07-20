"""Subdominio: Seguimiento Academico."""
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.desglose_por_area import DesglosePorArea
from app.dominio.seguimiento_academico.evolucion_nota import EvolucionNota
from app.dominio.seguimiento_academico.perfil_academico_repositorio import (
    IPerfilAcademicoMantenimiento,
    IPerfilAcademicoRepositorio,
)

__all__ = [
    "PerfilAcademico",
    "DesglosePorArea",
    "EvolucionNota",
    "IPerfilAcademicoRepositorio",
    "IPerfilAcademicoMantenimiento",
]
