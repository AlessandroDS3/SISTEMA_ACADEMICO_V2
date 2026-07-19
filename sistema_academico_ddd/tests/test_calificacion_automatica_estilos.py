"""Pruebas de los estilos agregados en Lab 10 sobre el subdominio
Calificacion_Automatica: Things (Calificacion.calcular),
Error/Exception Handling (reutiliza ExamenNoEncontradoError) y
Persistent-Tables (promedio y conteo agregados via SQL)."""
import pytest

from app.dominio.calificacion_automatica.calificacion import Calificacion
from app.dominio.gestion_examenes.excepciones import ExamenNoEncontradoError
from app.aplicacion.respuesta_estudiante_app_service import RespuestaEstudianteAppService
from app.infraestructura.repositorios.respuesta_estudiante_repositorio_impl import (
    RespuestaEstudianteRepositorioImpl,
)
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl


def test_calificacion_calcular_aplica_puntaje_y_penalizacion():
    calificacion = Calificacion.calcular(
        respuesta_id=1,
        numero_correctas=8,
        numero_incorrectas=2,
        numero_en_blanco=0,
        puntaje_por_pregunta=1.0,
        penalizacion_por_error=0.25,
    )

    assert calificacion.nota_final == pytest.approx(7.5)


def test_calificacion_calcular_nunca_da_nota_negativa():
    calificacion = Calificacion.calcular(
        respuesta_id=1,
        numero_correctas=0,
        numero_incorrectas=10,
        numero_en_blanco=0,
        puntaje_por_pregunta=1.0,
        penalizacion_por_error=1.0,
    )

    assert calificacion.nota_final == 0.0


def test_procesar_hoja_de_examen_inexistente_lanza_excepcion_de_dominio(app):
    servicio = RespuestaEstudianteAppService(
        RespuestaEstudianteRepositorioImpl(), ExamenRepositorioImpl()
    )

    with pytest.raises(ExamenNoEncontradoError):
        servicio.procesar_hoja_escaneada(examen_id=999, estudiante_id=1, ruta_imagen="x.jpg")


def test_promedio_y_conteo_por_examen_sin_calificaciones_son_neutros(app):
    repositorio = RespuestaEstudianteRepositorioImpl()

    assert repositorio.promedio_nota_por_examen(examen_id=999) == 0.0
    assert repositorio.contar_por_umbral_nota(examen_id=999, nota_minima_aprobatoria=11) == (0, 0)
