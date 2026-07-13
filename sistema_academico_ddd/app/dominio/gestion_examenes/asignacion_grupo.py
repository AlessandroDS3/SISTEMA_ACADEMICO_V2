"""Entidad de dominio AsignacionGrupo (grupo de estudiantes asignado a un Examen)."""
from app.extensions import db


class AsignacionGrupo(db.Model):
    __tablename__ = "asignaciones_grupo"

    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey("examenes.id"), nullable=False)
    nombre_grupo = db.Column(db.String(80), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    examen = db.relationship("Examen", back_populates="asignaciones")

    def __repr__(self) -> str:
        return f"<AsignacionGrupo grupo={self.nombre_grupo!r}>"
