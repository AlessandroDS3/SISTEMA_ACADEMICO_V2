"""Implementacion concreta de IUsuarioRepositorio usando SQLAlchemy
(equivalente al patron `@Repository` de JPA / DbContext de EF)."""
from typing import List, Optional

from app.extensions import db
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.usuario_repositorio import IUsuarioRepositorio


class UsuarioRepositorioImpl(IUsuarioRepositorio):

    def guardar(self, usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        return db.session.get(Usuario, id)

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        return db.session.query(Usuario).filter_by(username=username).first()

    def actualizar(self, usuario: Usuario) -> Usuario:
        db.session.commit()
        return usuario

    def eliminar(self, id: int) -> bool:
        usuario = self.buscar_por_id(id)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True

    def listar(self) -> List[Usuario]:
        return db.session.query(Usuario).all()
