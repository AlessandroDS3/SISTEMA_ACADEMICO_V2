"""Entidad de dominio PerfilAcademico (raiz de agregado del subdominio
Seguimiento_Academico): historial academico consolidado de un estudiante.
"""
from typing import Optional

from app.extensions import db
from app.dominio.seguimiento_academico.desglose_por_area import DesgloseporArea


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

    def desglose_de_area(self, area_id: int) -> Optional[DesgloseporArea]:
        """Estilo Things: el propio PerfilAcademico sabe buscar dentro
        de su coleccion de desgloses, en vez de que cada llamador
        repita el `next((d for d in perfil.desgloses_por_area if ...))`
        por su cuenta."""
        return next((d for d in self.desgloses_por_area if d.area_id == area_id), None)

    def __repr__(self) -> str:
        return f"<PerfilAcademico estudiante_id={self.estudiante_id} promedio={self.promedio_general}>"
