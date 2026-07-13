"""Implementacion concreta de IExamenRepositorio usando SQLAlchemy."""
from typing import List, Optional

from app.extensions import db
from app.dominio.gestion_examenes.examen import Examen
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio


class ExamenRepositorioImpl(IExamenRepositorio):

    def guardar(self, examen: Examen) -> Examen:
        db.session.add(examen)
        db.session.commit()
        return examen

    def buscar_por_id(self, id: int) -> Optional[Examen]:
        return db.session.get(Examen, id)

    def buscar_por_materia(self, materia_id: int) -> List[Examen]:
        return db.session.query(Examen).filter_by(materia_id=materia_id).all()

    def actualizar(self, examen: Examen) -> Examen:
        db.session.commit()
        return examen

    def eliminar(self, id: int) -> bool:
        examen = self.buscar_por_id(id)
        if examen is None:
            return False
        db.session.delete(examen)
        db.session.commit()
        return True

    def listar(self) -> List[Examen]:
        return db.session.query(Examen).all()
