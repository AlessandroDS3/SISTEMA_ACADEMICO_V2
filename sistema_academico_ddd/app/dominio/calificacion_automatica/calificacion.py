"""Entidad de dominio Calificacion (resultado de calificar una
RespuestaEstudiante contra el banco de PreguntaBanco del Examen).
"""
from app.extensions import db


class Calificacion(db.Model):
    __tablename__ = "calificaciones"

    id = db.Column(db.Integer, primary_key=True)
    respuesta_id = db.Column(
        db.Integer, db.ForeignKey("respuestas_estudiante.id"), nullable=False, unique=True
    )
    numero_correctas = db.Column(db.Integer, nullable=False, default=0)
    numero_incorrectas = db.Column(db.Integer, nullable=False, default=0)
    numero_en_blanco = db.Column(db.Integer, nullable=False, default=0)
    nota_final = db.Column(db.Float, nullable=False, default=0.0)

    respuesta = db.relationship("RespuestaEstudiante", back_populates="calificacion")

    def __repr__(self) -> str:
        return f"<Calificacion respuesta_id={self.respuesta_id} nota_final={self.nota_final}>"
