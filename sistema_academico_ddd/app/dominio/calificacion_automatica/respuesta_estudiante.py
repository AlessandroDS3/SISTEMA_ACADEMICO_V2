"""Entidad de dominio RespuestaEstudiante (hoja de respuestas escaneada
de un estudiante para un Examen).
"""
from datetime import datetime

from app.extensions import db


class RespuestaEstudiante(db.Model):
    __tablename__ = "respuestas_estudiante"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    respuestas_marcadas = db.Column(db.JSON, nullable=False, default=dict)  # {"1": "A", "2": "C", ...}
    ruta_imagen_original = db.Column(db.String(255))
    procesado_en = db.Column(db.DateTime, default=datetime.utcnow)

    calificacion = db.relationship(
        "Calificacion", back_populates="respuesta", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<RespuestaEstudiante examen_id={self.examen_id} estudiante_id={self.estudiante_id}>"
