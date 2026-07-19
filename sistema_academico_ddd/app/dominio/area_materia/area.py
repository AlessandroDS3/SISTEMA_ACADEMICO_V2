"""Entidad de dominio Area (subdominio Area_y_Materia)."""
from app.extensions import db
from app.dominio.area_materia.excepciones import MateriaDuplicadaError
from app.dominio.area_materia.materia import Materia


class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    materias = db.relationship("Materia", back_populates="area", cascade="all, delete-orphan")

    def agregar_materia(self, materia: Materia) -> None:
        """Estilo Things: el Area es quien conoce y protege el invariante
        "no dos materias con el mismo codigo dentro de la misma area",
        en vez de dejar que codigo externo manipule `self.materias`
        directamente y duplique esa regla en cada llamador."""
        if any(m.codigo == materia.codigo for m in self.materias):
            raise MateriaDuplicadaError(materia.codigo)
        materia.area = self
        self.materias.append(materia)

    def __repr__(self) -> str:
        return f"<Area id={self.id} nombre={self.nombre!r}>"
