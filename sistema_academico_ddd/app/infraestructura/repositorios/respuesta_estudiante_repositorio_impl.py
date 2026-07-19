"""Implementacion concreta de IRespuestaEstudianteRepositorio usando SQLAlchemy."""
from typing import List, Optional, Tuple

from sqlalchemy import func

from app.extensions import db
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion import Calificacion
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)


class RespuestaEstudianteRepositorioImpl(IRespuestaEstudianteRepositorio):

    def guardar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        db.session.add(respuesta)
        db.session.commit()
        return respuesta

    def buscar_por_id(self, respuesta_id: int) -> Optional[RespuestaEstudiante]:
        return db.session.get(RespuestaEstudiante, respuesta_id)

    def buscar_por_examen(self, examen_id: int) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).filter_by(examen_id=examen_id).all()

    def buscar_por_estudiante(self, estudiante_id: int) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).filter_by(estudiante_id=estudiante_id).all()

    def actualizar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        db.session.commit()
        return respuesta

    def eliminar(self, respuesta_id: int) -> bool:
        respuesta = self.buscar_por_id(respuesta_id)
        if respuesta is None:
            return False
        db.session.delete(respuesta)
        db.session.commit()
        return True

    def listar(self) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).all()

    def promedio_nota_por_examen(self, examen_id: int) -> float:
        """Estilo Persistent-Tables: `AVG` lo calcula la base de datos
        (una sola fila de vuelta), en vez de traer todas las
        Calificacion del examen y promediarlas con Python."""
        promedio = (
            db.session.query(func.avg(Calificacion.nota_final))
            .join(RespuestaEstudiante, Calificacion.respuesta_id == RespuestaEstudiante.id)
            .filter(RespuestaEstudiante.examen_id == examen_id)
            .scalar()
        )
        return float(promedio) if promedio is not None else 0.0

    def contar_por_umbral_nota(self, examen_id: int, nota_minima_aprobatoria: float) -> Tuple[int, int]:
        """Estilo Persistent-Tables: dos `COUNT` filtrados por umbral,
        en vez de cargar todas las notas y contarlas con `sum(1 for ...)`
        en Python."""
        base = (
            db.session.query(Calificacion)
            .join(RespuestaEstudiante, Calificacion.respuesta_id == RespuestaEstudiante.id)
            .filter(RespuestaEstudiante.examen_id == examen_id)
        )
        aprobados = base.filter(Calificacion.nota_final >= nota_minima_aprobatoria).count()
        desaprobados = base.filter(Calificacion.nota_final < nota_minima_aprobatoria).count()
        return aprobados, desaprobados
