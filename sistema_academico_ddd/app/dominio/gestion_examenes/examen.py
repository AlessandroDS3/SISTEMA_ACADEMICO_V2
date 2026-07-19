"""Entidad de dominio Examen (raiz de agregado del subdominio
Gestion_de_Examenes).
"""

from app.dominio.tiempo import ahora_utc
from app.extensions import db
from app.dominio.gestion_examenes.excepciones import PreguntaDuplicadaError
from app.dominio.gestion_examenes.pregunta_banco import PreguntaBanco


class Examen(db.Model):
    __tablename__ = "examenes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    creado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    creado_en = db.Column(db.DateTime, default=ahora_utc)
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

    def agregar_pregunta(self, pregunta: PreguntaBanco) -> None:
        """Estilo Things: el Examen es quien conoce y protege el
        invariante "no dos preguntas con el mismo numero en el banco",
        en vez de que la capa de aplicacion construya el objeto y lo
        anexe a `self.preguntas` sin validar nada."""
        if any(p.numero_pregunta == pregunta.numero_pregunta for p in self.preguntas):
            raise PreguntaDuplicadaError(pregunta.numero_pregunta)
        pregunta.examen = self
        self.preguntas.append(pregunta)

    def __repr__(self) -> str:
        return f"<Examen id={self.id} titulo={self.titulo!r}>"
