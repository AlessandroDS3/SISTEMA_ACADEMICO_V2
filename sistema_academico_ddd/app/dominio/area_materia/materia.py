"""Entidad de dominio Materia (subdominio Area_y_Materia)."""
from app.extensions import db


class Materia(db.Model):
    __tablename__ = "materias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=False)

    area = db.relationship("Area", back_populates="materias")

    def __repr__(self) -> str:
        return f"<Materia id={self.id} codigo={self.codigo!r}>"
