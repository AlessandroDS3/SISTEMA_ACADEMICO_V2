"""Application Service: casos de uso relacionados a Usuario
(registro, autenticacion, gestion de cuentas)."""
from typing import List, Optional

from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.autenticacion_usuarios.usuario_repositorio import IUsuarioRepositorio
from app.dominio.autenticacion_usuarios.excepciones import (
    UsernameEnUsoError,
    UsuarioNoEncontradoError,
)


class UsuarioAppService:
    """Orquesta el subdominio Autenticacion_y_Usuarios para la capa de
    presentacion. Depende de la ABSTRACCION `IUsuarioRepositorio`, no de
    la implementacion concreta (Dependency Inversion)."""

    def __init__(self, usuario_repositorio: IUsuarioRepositorio):
        self._repositorio = usuario_repositorio

    def registrar_usuario(self, username: str, password: str, rol: RolEnum) -> Usuario:
        if self._repositorio.buscar_por_username(username) is not None:
            raise UsernameEnUsoError(username)

        usuario = Usuario(username=username, rol=rol)
        usuario.establecer_password(password)
        return self._repositorio.guardar(usuario)

    def autenticar(self, username: str, password: str) -> Optional[Usuario]:
        usuario = self._repositorio.buscar_por_username(username)
        if usuario is not None and usuario.verificar_password(password):
            return usuario
        return None

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self._repositorio.buscar_por_id(usuario_id)

    def listar_usuarios(self) -> List[Usuario]:
        return self._repositorio.listar()

    def actualizar_usuario(
        self, usuario_id: int, username: str, rol: RolEnum, password: Optional[str] = None
    ) -> Usuario:
        usuario = self._repositorio.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(usuario_id)

        existente = self._repositorio.buscar_por_username(username)
        if existente is not None and existente.id != usuario_id:
            raise UsernameEnUsoError(username)

        usuario.actualizar_perfil(username, rol)
        if password:
            usuario.establecer_password(password)
        return self._repositorio.actualizar(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        return self._repositorio.eliminar(usuario_id)
