"""Pruebas de los estilos agregados en Lab 10 sobre Rankings y
Reportes_y_Estadisticas: Persistent-Tables (`top_n_por_examen`,
`contar_por_umbral_nota`), Lazy-Rivers (`iterar_por_examen`), Things
(`ReporteInstitucional.registrar_estadistica_grupo`) y
Error/Exception Handling (`ExamenNoEncontradoError` reutilizado)."""
import pytest

from app.extensions import db as _db
from app.dominio.area_materia.area import Area
from app.dominio.area_materia.materia import Materia
from app.dominio.gestion_examenes.examen_factory import ExamenFactory
from app.dominio.gestion_examenes.asignacion_grupo import AsignacionGrupo
from app.dominio.gestion_examenes.excepciones import ExamenNoEncontradoError
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion import Calificacion
from app.dominio.autenticacion_usuarios.usuario import Usuario
from app.dominio.autenticacion_usuarios.rol_enum import RolEnum
from app.aplicacion.ranking_app_service import RankingAppService
from app.aplicacion.reporte_institucional_app_service import ReporteInstitucionalAppService
from app.infraestructura.repositorios.ranking_repositorio_impl import (
    EntradaRankingRepositorioImpl,
)
from app.infraestructura.repositorios.respuesta_estudiante_repositorio_impl import (
    RespuestaEstudianteRepositorioImpl,
)
from app.infraestructura.repositorios.reporte_institucional_repositorio_impl import (
    ReporteInstitucionalRepositorioImpl,
)
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl


@pytest.fixture()
def examen_con_respuestas(app):
    area = Area(nombre="Ciencias")
    materia = Materia(nombre="Base de Datos", codigo="BD1", area=area)
    _db.session.add_all([area, materia])
    _db.session.commit()

    docente = Usuario(username="docente1", rol=RolEnum.DOCENTE)
    docente.establecer_password("clave123")
    _db.session.add(docente)
    _db.session.commit()

    examen = ExamenFactory.crear(
        titulo="Parcial 1", materia_id=materia.id, creado_por_id=docente.id, numero_preguntas=10
    )
    _db.session.add(examen)
    _db.session.commit()

    asignacion = AsignacionGrupo(examen_id=examen.id, nombre_grupo="A", docente_id=docente.id)
    _db.session.add(asignacion)

    for indice, (username, nota) in enumerate(
        [("est1", 15.0), ("est2", 8.0), ("est3", 18.0)]
    ):
        estudiante = Usuario(username=username, rol=RolEnum.ESTUDIANTE)
        estudiante.establecer_password("clave123")
        _db.session.add(estudiante)
        _db.session.flush()

        respuesta = RespuestaEstudiante(
            examen_id=examen.id, estudiante_id=estudiante.id, respuestas_marcadas={}
        )
        _db.session.add(respuesta)
        _db.session.flush()

        calificacion = Calificacion.calcular(
            respuesta_id=respuesta.id,
            numero_correctas=0,
            numero_incorrectas=0,
            numero_en_blanco=10,
            puntaje_por_pregunta=1.0,
            penalizacion_por_error=0.0,
        )
        calificacion.nota_final = nota
        _db.session.add(calificacion)

    _db.session.commit()
    return examen


def test_generar_ranking_ordena_por_nota_descendente(app, examen_con_respuestas):
    servicio = RankingAppService(
        EntradaRankingRepositorioImpl(), RespuestaEstudianteRepositorioImpl()
    )

    entradas = servicio.generar_ranking(examen_con_respuestas.id)

    notas = [entrada.nota_final for entrada in entradas]
    assert notas == sorted(notas, reverse=True)


def test_obtener_top_aplica_order_by_y_limit_en_sql(app, examen_con_respuestas):
    servicio = RankingAppService(
        EntradaRankingRepositorioImpl(), RespuestaEstudianteRepositorioImpl()
    )
    servicio.generar_ranking(examen_con_respuestas.id)

    top1 = servicio.obtener_top(examen_con_respuestas.id, n=1)

    assert len(top1) == 1
    assert top1[0].nota_final == 18.0


def test_iterar_ranking_completo_es_un_generador_perezoso(app, examen_con_respuestas):
    servicio = RankingAppService(
        EntradaRankingRepositorioImpl(), RespuestaEstudianteRepositorioImpl()
    )
    servicio.generar_ranking(examen_con_respuestas.id)

    flujo = servicio.iterar_ranking_completo(examen_con_respuestas.id)

    assert hasattr(flujo, "__next__")
    assert len(list(flujo)) == 3


def test_generar_reporte_de_examen_inexistente_lanza_excepcion_de_dominio(app):
    servicio = ReporteInstitucionalAppService(
        ReporteInstitucionalRepositorioImpl(),
        RespuestaEstudianteRepositorioImpl(),
        ExamenRepositorioImpl(),
    )

    with pytest.raises(ExamenNoEncontradoError):
        servicio.generar_reporte(999)


def test_generar_reporte_registra_estadisticas_por_grupo_via_la_entidad(app, examen_con_respuestas):
    servicio = ReporteInstitucionalAppService(
        ReporteInstitucionalRepositorioImpl(),
        RespuestaEstudianteRepositorioImpl(),
        ExamenRepositorioImpl(),
    )

    reporte = servicio.generar_reporte(examen_con_respuestas.id)

    assert reporte.id is not None
    assert len(reporte.estadisticas_grupales) == 1
    estadistica = reporte.estadisticas_grupales[0]
    assert estadistica.numero_aprobados == 2
    assert estadistica.numero_desaprobados == 1
