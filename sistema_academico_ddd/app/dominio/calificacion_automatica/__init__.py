"""Subdominio: Calificacion Automatica."""
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion import Calificacion
from app.dominio.calificacion_automatica.calificacion_servicio import CalificacionServicio
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)

__all__ = [
    "RespuestaEstudiante",
    "Calificacion",
    "CalificacionServicio",
    "IRespuestaEstudianteRepositorio",
]
