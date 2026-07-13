"""Entidad de dominio Examen (raiz de agregado del subdominio
Gestion_de_Examenes).
"""
from datetime import datetime

from app.extensions import db
from app.dominio.area_materia.materia import Materia  # noqa: F401 (relacion)


class Examen(db.Model):
    __tablename__ = "examenes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    creado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    numero_preguntas = db.Column(db.Integer, nullable=False, default=0)

    materia = db.relationship("Materia")
    preguntas = db.relationship(
        "PreguntaBanco", back_populates="examen", cascade="all, delete-orphan"
    )
    asignaciones = db.relationship(
        "AsignacionGrupo", back_populates="examen", cascade="all, delete-orphan"
    )
    configuracion = db.relationship(
        "ConfiguracionExamen",
        back_populates="examen",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Examen id={self.id} titulo={self.titulo!r}>"
