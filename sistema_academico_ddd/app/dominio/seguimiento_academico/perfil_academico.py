"""Entidad de dominio PerfilAcademico (raiz de agregado del subdominio
Seguimiento_Academico): historial academico consolidado de un estudiante.
"""
from app.extensions import db


class PerfilAcademico(db.Model):
    __tablename__ = "perfiles_academicos"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False, unique=True)
    promedio_general = db.Column(db.Float, nullable=False, default=0.0)

    desgloses_por_area = db.relationship(
        "DesgloseporArea", back_populates="perfil", cascade="all, delete-orphan"
    )
    evoluciones_nota = db.relationship(
        "EvolucionNota", back_populates="perfil", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<PerfilAcademico estudiante_id={self.estudiante_id} promedio={self.promedio_general}>"
