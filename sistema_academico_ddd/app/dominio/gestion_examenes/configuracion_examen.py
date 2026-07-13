"""Value Object ConfiguracionExamen (embebido en Examen)."""
from app.extensions import db


class ConfiguracionExamen(db.Model):
    __tablename__ = "configuraciones_examen"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False, unique=True)
    numero_alternativas = db.Column(db.Integer, nullable=False, default=4)
    puntaje_por_pregunta = db.Column(db.Float, nullable=False, default=1.0)
    penalizacion_por_error = db.Column(db.Float, nullable=False, default=0.0)
    tiempo_limite_minutos = db.Column(db.Integer, nullable=True)

    examen = db.relationship("Examen", back_populates="configuracion")
