"""Entidad de dominio Area (subdominio Area_y_Materia)."""
from app.extensions import db


class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    materias = db.relationship("Materia", back_populates="area", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Area id={self.id} nombre={self.nombre!r}>"
