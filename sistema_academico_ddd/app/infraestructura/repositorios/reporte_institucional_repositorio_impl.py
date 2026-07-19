"""Implementacion concreta de IReporteInstitucionalRepositorio usando SQLAlchemy."""
import math
from typing import List, Optional, Tuple

from sqlalchemy import func

from app.extensions import db
from app.dominio.calificacion_automatica.calificacion import Calificacion
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional
from app.dominio.reportes_estadisticas.reporte_institucional_repositorio import (
    IReporteInstitucionalRepositorio,
)


class ReporteInstitucionalRepositorioImpl(IReporteInstitucionalRepositorio):

    def guardar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        db.session.add(reporte)
        db.session.commit()
        return reporte

    def buscar_por_id(self, reporte_id: int) -> Optional[ReporteInstitucional]:
        return db.session.get(ReporteInstitucional, reporte_id)

    def buscar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        return db.session.query(ReporteInstitucional).filter_by(examen_id=examen_id).all()

    def estadisticas_nota_por_examen(self, examen_id: int) -> Tuple[float, float]:
        """Estilo Persistent-Tables: el promedio y la desviacion estandar
        de las notas de un examen se calculan con agregaciones SQL
        (`AVG`) sobre la tabla de calificaciones, en vez de traer todas
        las notas a memoria y recorrerlas en Python con `statistics`.

        La desviacion poblacional se deriva de dos promedios pedidos en
        la misma consulta: ``sqrt(AVG(nota^2) - AVG(nota)^2)``.
        """
        promedio_nota, promedio_cuadrados = (
            db.session.query(
                func.avg(Calificacion.nota_final),
                func.avg(Calificacion.nota_final * Calificacion.nota_final),
            )
            .join(RespuestaEstudiante, Calificacion.respuesta_id == RespuestaEstudiante.id)
            .filter(RespuestaEstudiante.examen_id == examen_id)
            .one()
        )

        if promedio_nota is None:
            return 0.0, 0.0

        promedio = float(promedio_nota)
        varianza = float(promedio_cuadrados) - promedio * promedio
        return promedio, math.sqrt(max(varianza, 0.0))

    def actualizar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        db.session.commit()
        return reporte

    def eliminar(self, reporte_id: int) -> bool:
        reporte = self.buscar_por_id(reporte_id)
        if reporte is None:
            return False
        db.session.delete(reporte)
        db.session.commit()
        return True

    def listar(self) -> List[ReporteInstitucional]:
        return db.session.query(ReporteInstitucional).all()
