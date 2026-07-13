"""Implementacion concreta de IRespuestaEstudianteRepositorio usando SQLAlchemy."""
from typing import List, Optional

from app.extensions import db
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)


class RespuestaEstudianteRepositorioImpl(IRespuestaEstudianteRepositorio):

    def guardar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        db.session.add(respuesta)
        db.session.commit()
        return respuesta

    def buscar_por_id(self, id: int) -> Optional[RespuestaEstudiante]:
        return db.session.get(RespuestaEstudiante, id)

    def buscar_por_examen(self, examen_id: int) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).filter_by(examen_id=examen_id).all()

    def buscar_por_estudiante(self, estudiante_id: int) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).filter_by(estudiante_id=estudiante_id).all()

    def actualizar(self, respuesta: RespuestaEstudiante) -> RespuestaEstudiante:
        db.session.commit()
        return respuesta

    def eliminar(self, id: int) -> bool:
        respuesta = self.buscar_por_id(id)
        if respuesta is None:
            return False
        db.session.delete(respuesta)
        db.session.commit()
        return True

    def listar(self) -> List[RespuestaEstudiante]:
        return db.session.query(RespuestaEstudiante).all()
