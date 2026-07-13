"""Pruebas de integracion del ExamenAppService contra una base de
datos real (SQLite temporal).
"""
import pytest

from app.extensions import db as _db
from app.aplicacion.examen_app_service import ExamenAppService
from app.aplicacion.usuario_app_service import UsuarioAppService
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl
from app.infraestructura.repositorios.usuario_repositorio_impl import UsuarioRepositorioImpl
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.dominio.area_materia.area import Area
from app.dominio.area_materia.materia import Materia


@pytest.fixture()
def servicio(app):
    return ExamenAppService(ExamenRepositorioImpl())


@pytest.fixture()
def materia(app):
    area = Area(nombre="Ciencias de la Computacion")
    materia = Materia(nombre="Base de Datos II", codigo="BD2", area=area)
    _db.session.add_all([area, materia])
    _db.session.commit()
    return materia


@pytest.fixture()
def docente(app):
    servicio_usuario = UsuarioAppService(UsuarioRepositorioImpl())
    return servicio_usuario.registrar_usuario("docente1", "clave123", RolEnum.DOCENTE)


def test_crear_examen_lo_persiste_con_su_configuracion(servicio, materia, docente):
    examen = servicio.crear_examen(
        titulo="Parcial 1",
        materia_id=materia.id,
        creado_por_id=docente.id,
        numero_preguntas=20,
        numero_alternativas=4,
        puntaje_por_pregunta=1.0,
    )

    assert examen.id is not None
    assert examen.configuracion is not None
    assert examen.configuracion.numero_alternativas == 4


def test_actualizar_examen_cambia_titulo_y_configuracion(servicio, materia, docente):
    examen = servicio.crear_examen(
        titulo="Parcial 1",
        materia_id=materia.id,
        creado_por_id=docente.id,
        numero_preguntas=20,
    )

    actualizado = servicio.actualizar_examen(
        examen.id,
        titulo="Parcial 1 - Revisado",
        materia_id=materia.id,
        numero_preguntas=25,
        numero_alternativas=5,
        puntaje_por_pregunta=2.0,
    )

    assert actualizado.titulo == "Parcial 1 - Revisado"
    assert actualizado.numero_preguntas == 25
    assert actualizado.configuracion.numero_alternativas == 5
    assert actualizado.configuracion.puntaje_por_pregunta == 2.0


def test_actualizar_examen_inexistente_falla(servicio):
    with pytest.raises(ValueError):
        servicio.actualizar_examen(999, titulo="X", materia_id=1, numero_preguntas=1)


def test_eliminar_examen_lo_quita_del_listado(servicio, materia, docente):
    examen = servicio.crear_examen(
        titulo="Parcial 1", materia_id=materia.id, creado_por_id=docente.id, numero_preguntas=20
    )

    assert servicio.eliminar_examen(examen.id) is True
    assert servicio.listar_examenes() == []
