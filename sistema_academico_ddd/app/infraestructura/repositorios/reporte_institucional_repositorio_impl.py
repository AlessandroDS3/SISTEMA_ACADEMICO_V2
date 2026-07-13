"""Implementacion concreta de IReporteInstitucionalRepositorio usando SQLAlchemy."""
from typing import List, Optional

from app.extensions import db
from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional
from app.dominio.reportes_estadisticas.reporte_institucional_repositorio import (
    IReporteInstitucionalRepositorio,
)


class ReporteInstitucionalRepositorioImpl(IReporteInstitucionalRepositorio):

    def guardar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        db.session.add(reporte)
        db.session.commit()
        return reporte

    def buscar_por_id(self, id: int) -> Optional[ReporteInstitucional]:
        return db.session.get(ReporteInstitucional, id)

    def buscar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        return db.session.query(ReporteInstitucional).filter_by(examen_id=examen_id).all()

    def actualizar(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        db.session.commit()
        return reporte

    def eliminar(self, id: int) -> bool:
        reporte = self.buscar_por_id(id)
        if reporte is None:
            return False
        db.session.delete(reporte)
        db.session.commit()
        return True

    def listar(self) -> List[ReporteInstitucional]:
        return db.session.query(ReporteInstitucional).all()
