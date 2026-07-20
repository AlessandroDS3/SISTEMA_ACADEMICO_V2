"""Implementacion concreta de IPerfilAcademicoRepositorio e
IPerfilAcademicoMantenimiento usando SQLAlchemy.

Una unica clase concreta puede implementar varias interfaces pequeñas;
el Principio de Segregacion de Interfaces separa los *contratos* segun
quien los consume, no obliga a partir la implementacion en varias
clases."""
from typing import List, Optional

from app.extensions import db
from app.dominio.seguimiento_academico.excepciones import PerfilNoEncontradoError
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.perfil_academico_repositorio import (
    IPerfilAcademicoMantenimiento,
    IPerfilAcademicoRepositorio,
)


class PerfilAcademicoRepositorioImpl(
    IPerfilAcademicoRepositorio, IPerfilAcademicoMantenimiento
):

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

    def eliminar(self, perfil_id: int) -> None:
        perfil = self.buscar_por_id(perfil_id)
        if perfil is None:
            raise PerfilNoEncontradoError(perfil_id)
        db.session.delete(perfil)
        db.session.commit()

    def listar(self) -> List[PerfilAcademico]:
        return db.session.query(PerfilAcademico).all()
