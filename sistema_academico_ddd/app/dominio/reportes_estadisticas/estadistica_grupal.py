"""Entidad de dominio EstadisticaGrupal (estadisticas de un
AsignacionGrupo dentro de un ReporteInstitucional)."""
from app.extensions import db


class EstadisticaGrupal(db.Model):
    __tablename__ = "estadisticas_grupales"

    id = db.Column(db.Integer, primary_key=True)
    reporte_id = db.Column(db.Integer, db.ForeignKey("reportes_institucionales.id"), nullable=False)
    asignacion_grupo_id = db.Column(
        db.Integer, db.ForeignKey("asignaciones_grupo.id"), nullable=False
    )
    promedio_grupo = db.Column(db.Float, nullable=False, default=0.0)
    numero_aprobados = db.Column(db.Integer, nullable=False, default=0)
    numero_desaprobados = db.Column(db.Integer, nullable=False, default=0)

    reporte = db.relationship("ReporteInstitucional", back_populates="estadisticas_grupales")
    asignacion_grupo = db.relationship("AsignacionGrupo")
