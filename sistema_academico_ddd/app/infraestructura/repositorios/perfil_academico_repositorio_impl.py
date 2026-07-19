"""Implementacion concreta de IPerfilAcademicoRepositorio usando SQLAlchemy."""
from typing import List, Optional

from app.extensions import db
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.perfil_academico_repositorio import (
    IPerfilAcademicoRepositorio,
)


class PerfilAcademicoRepositorioImpl(IPerfilAcademicoRepositorio):

    def guardar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        db.session.add(perfil)
        db.session.commit()
        return perfil

    def buscar_por_id(self, perfil_id: int) -> Optional[PerfilAcademico]:
        return db.session.get(PerfilAcademico, perfil_id)

    def buscar_por_estudiante(self, estudiante_id: int) -> Optional[PerfilAcademico]:
        return db.session.query(PerfilAcademico).filter_by(estudiante_id=estudiante_id).first()

    def actualizar(self, perfil: PerfilAcademico) -> PerfilAcademico:
        db.session.commit()
        return perfil

    def eliminar(self, perfil_id: int) -> bool:
        perfil = self.buscar_por_id(perfil_id)
        if perfil is None:
            return False
        db.session.delete(perfil)
        db.session.commit()
        return True

    def listar(self) -> List[PerfilAcademico]:
        return db.session.query(PerfilAcademico).all()
