"""Pruebas unitarias de los estilos agregados en Lab 10 sobre la
entidad Usuario: Error/Exception Handling (excepciones de dominio
propias) y Things (comportamiento encapsulado en la entidad).
"""
import pytest

from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.autenticacion_usuarios.excepciones import PasswordInvalidoError


def test_establecer_password_muy_corto_lanza_excepcion_de_dominio():
    usuario = Usuario(username="camila", rol=RolEnum.DOCENTE)

    with pytest.raises(PasswordInvalidoError):
        usuario.establecer_password("123")


def test_actualizar_perfil_cambia_username_y_rol_desde_la_propia_entidad():
    usuario = Usuario(username="camila", rol=RolEnum.ESTUDIANTE)

    usuario.actualizar_perfil("camila_docente", RolEnum.DOCENTE)

    assert usuario.username == "camila_docente"
    assert usuario.rol == RolEnum.DOCENTE
