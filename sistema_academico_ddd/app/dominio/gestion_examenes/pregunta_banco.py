"""Entidad de dominio PreguntaBanco (banco de preguntas de un Examen)."""
from app.extensions import db


class PreguntaBanco(db.Model):
    __tablename__ = "preguntas_banco"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    numero_pregunta = db.Column(db.Integer, nullable=False)
    respuesta_correcta = db.Column(db.String(5), nullable=False)  # p.ej. "A", "B", "C", "D"
    enunciado = db.Column(db.Text)

    examen = db.relationship("Examen", back_populates="preguntas")

    def __repr__(self) -> str:
        return f"<PreguntaBanco n={self.numero_pregunta} correcta={self.respuesta_correcta!r}>"
