"""Entidad de dominio ReporteInstitucional (raiz de agregado del
subdominio Reportes_y_Estadisticas)."""
from datetime import datetime

from app.extensions import db


class ReporteInstitucional(db.Model):
    __tablename__ = "reportes_institucionales"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    generado_en = db.Column(db.DateTime, default=datetime.utcnow)
    promedio_general = db.Column(db.Float, nullable=False, default=0.0)
    desviacion_estandar = db.Column(db.Float, nullable=False, default=0.0)

    estadisticas_grupales = db.relationship(
        "EstadisticaGrupal", back_populates="reporte", cascade="all, delete-orphan"
    )
    examen = db.relationship("Examen")
