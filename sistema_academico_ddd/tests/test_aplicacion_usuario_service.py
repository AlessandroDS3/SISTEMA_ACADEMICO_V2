"""Pruebas de integracion del UsuarioAppService contra una base de
datos real (SQLite temporal), pasando por el repositorio concreto.
"""
import pytest

from app.aplicacion.usuario_app_service import UsuarioAppService
from app.infraestructura.repositorios.usuario_repositorio_impl import UsuarioRepositorioImpl
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum


@pytest.fixture()
def servicio(app):
    return UsuarioAppService(UsuarioRepositorioImpl())


def test_registrar_usuario_lo_persiste(servicio):
    usuario = servicio.registrar_usuario("camila", "clave123", RolEnum.DOCENTE)

    assert usuario.id is not None
    assert servicio.listar_usuarios() == [usuario]


def test_registrar_usuario_con_username_repetido_falla(servicio):
    servicio.registrar_usuario("camila", "clave123", RolEnum.DOCENTE)

    with pytest.raises(ValueError):
        servicio.registrar_usuario("camila", "otra-clave", RolEnum.ESTUDIANTE)


def test_autenticar_con_credenciales_correctas_retorna_el_usuario(servicio):
    servicio.registrar_usuario("camila", "clave123", RolEnum.DOCENTE)

    autenticado = servicio.autenticar("camila", "clave123")

    assert autenticado is not None
    assert autenticado.username == "camila"


def test_autenticar_con_password_incorrecto_retorna_none(servicio):
    servicio.registrar_usuario("camila", "clave123", RolEnum.DOCENTE)

    assert servicio.autenticar("camila", "clave-equivocada") is None


def test_actualizar_usuario_cambia_username_y_rol(servicio):
    usuario = servicio.registrar_usuario("camila", "clave123", RolEnum.ESTUDIANTE)

    actualizado = servicio.actualizar_usuario(
        usuario.id, username="camila_docente", rol=RolEnum.DOCENTE
    )

    assert actualizado.username == "camila_docente"
    assert actualizado.rol == RolEnum.DOCENTE


def test_actualizar_usuario_sin_password_no_cambia_el_hash(servicio):
    usuario = servicio.registrar_usuario("camila", "clave123", RolEnum.ESTUDIANTE)
    hash_original = usuario.password_hash

    actualizado = servicio.actualizar_usuario(usuario.id, username="camila", rol=RolEnum.ESTUDIANTE)

    assert actualizado.password_hash == hash_original


def test_actualizar_usuario_inexistente_falla(servicio):
    with pytest.raises(ValueError):
        servicio.actualizar_usuario(999, username="nadie", rol=RolEnum.ESTUDIANTE)


def test_eliminar_usuario_lo_quita_del_listado(servicio):
    usuario = servicio.registrar_usuario("camila", "clave123", RolEnum.ESTUDIANTE)

    eliminado = servicio.eliminar_usuario(usuario.id)

    assert eliminado is True
    assert servicio.listar_usuarios() == []
