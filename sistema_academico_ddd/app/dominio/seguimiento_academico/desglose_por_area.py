"""Entidad de dominio DesglosePorArea (rendimiento agregado por Area
dentro de un PerfilAcademico)."""
from app.extensions import db


class DesglosePorArea(db.Model):
    __tablename__ = "desgloses_por_area"

    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfiles_academicos.id"), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=False)
    promedio_area = db.Column(db.Float, nullable=False, default=0.0)

    perfil = db.relationship("PerfilAcademico", back_populates="desgloses_por_area")
    area = db.relationship("Area")
