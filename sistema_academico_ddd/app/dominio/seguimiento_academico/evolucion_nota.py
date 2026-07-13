"""Entidad de dominio EvolucionNota (nota historica de un Examen dentro
del PerfilAcademico de un estudiante, usada para graficar su evolucion)."""
from datetime import datetime

from app.extensions import db


class EvolucionNota(db.Model):
    __tablename__ = "evoluciones_nota"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfiles_academicos.id"), nullable=False)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    nota_final = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    perfil = db.relationship("PerfilAcademico", back_populates="evoluciones_nota")
    examen = db.relationship("Examen")
