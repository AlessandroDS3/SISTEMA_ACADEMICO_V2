"""Pruebas de los estilos agregados en Lab 10 sobre ExamenAppService:
Cookbook (crear_examen/actualizar_examen como receta de pasos con
nombre propio), Error/Exception Handling (excepciones de dominio),
Things (Examen.agregar_pregunta protege su invariante) y
Persistent-Tables (conteo de preguntas via SQL)."""
import pytest

from app.aplicacion.examen_app_service import ExamenAppService
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl
from app.dominio.gestion_examenes.excepciones import (
    ExamenNoEncontradoError,
    NumeroPreguntasInvalidoError,
    PreguntaDuplicadaError,
)


@pytest.fixture()
def servicio(app):
    return ExamenAppService(ExamenRepositorioImpl())


def test_crear_examen_con_numero_preguntas_invalido_lanza_excepcion_de_dominio(servicio):
    with pytest.raises(NumeroPreguntasInvalidoError):
        servicio.crear_examen(
            titulo="Parcial 1", materia_id=1, creado_por_id=1, numero_preguntas=0
        )


def test_actualizar_examen_inexistente_lanza_excepcion_de_dominio(servicio):
    with pytest.raises(ExamenNoEncontradoError):
        servicio.actualizar_examen(999, titulo="X", materia_id=1, numero_preguntas=1)


def test_agregar_pregunta_al_banco_incrementa_el_conteo_agregado(servicio):
    examen = servicio.crear_examen(
        titulo="Parcial 1", materia_id=1, creado_por_id=1, numero_preguntas=2
    )

    servicio.agregar_pregunta_al_banco(examen.id, numero_pregunta=1, respuesta_correcta="A")
    servicio.agregar_pregunta_al_banco(examen.id, numero_pregunta=2, respuesta_correcta="B")

    repositorio = ExamenRepositorioImpl()
    assert repositorio.contar_preguntas_por_examen(examen.id) == 2


def test_agregar_pregunta_con_numero_repetido_lanza_excepcion_de_dominio(servicio):
    examen = servicio.crear_examen(
        titulo="Parcial 1", materia_id=1, creado_por_id=1, numero_preguntas=2
    )
    servicio.agregar_pregunta_al_banco(examen.id, numero_pregunta=1, respuesta_correcta="A")

    with pytest.raises(PreguntaDuplicadaError):
        servicio.agregar_pregunta_al_banco(examen.id, numero_pregunta=1, respuesta_correcta="C")
