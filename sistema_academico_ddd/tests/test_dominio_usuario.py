"""Pruebas unitarias de la entidad de dominio Usuario.

No requieren base de datos: solo verifican el comportamiento propio
de la entidad (hash de password), que es logica de dominio pura.
"""
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum


def test_establecer_password_guarda_un_hash_no_el_texto_plano():
    usuario = Usuario(username="camila", rol=RolEnum.DOCENTE)

    usuario.establecer_password("clave123")

    assert usuario.password_hash != "clave123"
    assert usuario.password_hash is not None


def test_verificar_password_acepta_la_clave_correcta():
    usuario = Usuario(username="camila", rol=RolEnum.DOCENTE)
    usuario.establecer_password("clave123")

    assert usuario.verificar_password("clave123") is True


def test_verificar_password_rechaza_una_clave_incorrecta():
    usuario = Usuario(username="camila", rol=RolEnum.DOCENTE)
    usuario.establecer_password("clave123")

    assert usuario.verificar_password("otra-clave") is False
