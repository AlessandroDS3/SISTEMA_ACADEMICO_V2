"""Implementacion concreta de IUsuarioRepositorio usando SQLAlchemy
(equivalente al patron `@Repository` de JPA / DbContext de EF)."""
from typing import Dict, Iterator, List, Optional

from sqlalchemy import func

from app.extensions import db
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.autenticacion_usuarios.usuario_repositorio import IUsuarioRepositorio


class UsuarioRepositorioImpl(IUsuarioRepositorio):

    def guardar(self, usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return db.session.get(Usuario, usuario_id)

    def buscar_por_username(self, username: str) -> Optional[Usuario]:
        return db.session.query(Usuario).filter_by(username=username).first()

    def actualizar(self, usuario: Usuario) -> Usuario:
        db.session.commit()
        return usuario

    def eliminar(self, usuario_id: int) -> bool:
        usuario = self.buscar_por_id(usuario_id)
        if usuario is None:
            return False
        db.session.delete(usuario)
        db.session.commit()
        return True

    def listar(self) -> List[Usuario]:
        return db.session.query(Usuario).all()

    def contar_por_rol(self) -> Dict[RolEnum, int]:
        """Estilo Persistent-Tables: `GROUP BY` lo resuelve la base de
        datos en una sola consulta, en vez de traer todos los usuarios
        y contarlos con un `Counter`/`for` en Python."""
        filas = db.session.query(Usuario.rol, func.count(Usuario.id)).group_by(Usuario.rol).all()
        return {rol: cantidad for rol, cantidad in filas}

    def iterar_todos(self) -> Iterator[Usuario]:
        """Estilo Lazy-Rivers: generador que trae los usuarios de la
        base de datos en lotes (`yield_per`) a medida que se consumen,
        en vez de materializar la tabla completa con `.all()` antes de
        poder empezar a iterar."""
        for usuario in db.session.query(Usuario).yield_per(50):
            yield usuario
