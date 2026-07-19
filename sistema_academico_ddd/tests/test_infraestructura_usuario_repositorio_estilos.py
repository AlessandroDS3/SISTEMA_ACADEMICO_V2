"""Pruebas de integracion de los estilos Persistent-Tables
(`contar_por_rol`) y Lazy-Rivers (`iterar_todos`) agregados en Lab 10
sobre UsuarioRepositorioImpl."""
from app.infraestructura.repositorios.usuario_repositorio_impl import UsuarioRepositorioImpl
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum


def _crear_usuario(username: str, rol: RolEnum) -> Usuario:
    usuario = Usuario(username=username, rol=rol)
    usuario.establecer_password("clave123")
    return usuario


def test_contar_por_rol_agrega_con_sql_group_by(app):
    repositorio = UsuarioRepositorioImpl()
    repositorio.guardar(_crear_usuario("camila", RolEnum.DOCENTE))
    repositorio.guardar(_crear_usuario("ana", RolEnum.DOCENTE))
    repositorio.guardar(_crear_usuario("luis", RolEnum.ESTUDIANTE))

    conteo = repositorio.contar_por_rol()

    assert conteo[RolEnum.DOCENTE] == 2
    assert conteo[RolEnum.ESTUDIANTE] == 1


def test_iterar_todos_es_un_generador_perezoso(app):
    repositorio = UsuarioRepositorioImpl()
    repositorio.guardar(_crear_usuario("camila", RolEnum.DOCENTE))
    repositorio.guardar(_crear_usuario("ana", RolEnum.ESTUDIANTE))

    flujo = repositorio.iterar_todos()

    assert hasattr(flujo, "__next__")  # es un generador, no una lista materializada
    usernames = {usuario.username for usuario in flujo}
    assert usernames == {"camila", "ana"}
