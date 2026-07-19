"""Pruebas de los estilos agregados en Lab 10 sobre
Seguimiento_Academico: Cookbook (registrar_resultado_examen como
receta), Trinity (Estado/Lector/Escritor para recalcular el
promedio), Error/Exception Handling (NotaInvalidaError) y Things
(PerfilAcademico.desglose_de_area)."""
import pytest

from app.aplicacion.perfil_academico_app_service import PerfilAcademicoAppService
from app.infraestructura.repositorios.perfil_academico_repositorio_impl import (
    PerfilAcademicoRepositorioImpl,
)
from app.infraestructura.repositorios.respuesta_estudiante_repositorio_impl import (
    RespuestaEstudianteRepositorioImpl,
)
from app.dominio.seguimiento_academico.excepciones import NotaInvalidaError
from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico
from app.dominio.seguimiento_academico.desglose_por_area import DesgloseporArea


@pytest.fixture()
def servicio(app):
    return PerfilAcademicoAppService(
        PerfilAcademicoRepositorioImpl(), RespuestaEstudianteRepositorioImpl()
    )


def test_registrar_resultado_examen_recalcula_el_promedio_via_trinity(servicio):
    perfil = servicio.registrar_resultado_examen(estudiante_id=1, examen_id=1, nota_final=16.0)
    assert perfil.promedio_general == 16.0

    perfil = servicio.registrar_resultado_examen(estudiante_id=1, examen_id=2, nota_final=10.0)
    assert perfil.promedio_general == 13.0


def test_registrar_resultado_examen_con_nota_fuera_de_rango_lanza_excepcion_de_dominio(servicio):
    with pytest.raises(NotaInvalidaError):
        servicio.registrar_resultado_examen(estudiante_id=1, examen_id=1, nota_final=25.0)


def test_desglose_de_area_encuentra_el_desglose_correspondiente():
    perfil = PerfilAcademico(estudiante_id=1)
    desglose = DesgloseporArea(area_id=5, promedio_area=14.0)
    perfil.desgloses_por_area.append(desglose)

    assert perfil.desglose_de_area(5) is desglose
    assert perfil.desglose_de_area(999) is None
