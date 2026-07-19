"""Entidad de dominio Calificacion (resultado de calificar una
RespuestaEstudiante contra el banco de PreguntaBanco del Examen).
"""
from app.extensions import db


class Calificacion(db.Model):
    __tablename__ = "calificaciones"

    id = db.Column(db.Integer, primary_key=True)
    respuesta_id = db.Column(
        db.Integer, db.ForeignKey("respuestas_estudiante.id"), nullable=False, unique=True
    )
    numero_correctas = db.Column(db.Integer, nullable=False, default=0)
    numero_incorrectas = db.Column(db.Integer, nullable=False, default=0)
    numero_en_blanco = db.Column(db.Integer, nullable=False, default=0)
    nota_final = db.Column(db.Float, nullable=False, default=0.0)

    respuesta = db.relationship("RespuestaEstudiante", back_populates="calificacion")

    @classmethod
    def calcular(
        cls,
        respuesta_id: int,
        numero_correctas: int,
        numero_incorrectas: int,
        numero_en_blanco: int,
        puntaje_por_pregunta: float,
        penalizacion_por_error: float,
    ) -> "Calificacion":
        """Estilo Things: la propia Calificacion sabe derivar su
        `nota_final` a partir de los conteos (correctas/incorrectas) y
        la configuracion del examen. Quien cuenta las respuestas
        (`CalificacionServicio`, que compara contra el banco de
        preguntas) no necesita conocer la formula de puntaje."""
        puntaje = numero_correctas * puntaje_por_pregunta
        puntaje -= numero_incorrectas * penalizacion_por_error
        return cls(
            respuesta_id=respuesta_id,
            numero_correctas=numero_correctas,
            numero_incorrectas=numero_incorrectas,
            numero_en_blanco=numero_en_blanco,
            nota_final=max(puntaje, 0.0),
        )

    def __repr__(self) -> str:
        return f"<Calificacion respuesta_id={self.respuesta_id} nota_final={self.nota_final}>"
