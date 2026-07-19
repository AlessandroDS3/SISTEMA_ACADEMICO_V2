"""Contenedor de dependencias muy simple (poor-man's DI).

Conecta las implementaciones concretas de infraestructura con los
Application Services, para que los Controllers no tengan que conocer
las clases de infraestructura directamente.
"""
from app.aplicacion.usuario_app_service import UsuarioAppService
from app.aplicacion.examen_app_service import ExamenAppService
from app.aplicacion.respuesta_estudiante_app_service import RespuestaEstudianteAppService
from app.aplicacion.perfil_academico_app_service import PerfilAcademicoAppService
from app.aplicacion.reporte_institucional_app_service import ReporteInstitucionalAppService
from app.aplicacion.ranking_app_service import RankingAppService

from app.infraestructura.repositorios.usuario_repositorio_impl import UsuarioRepositorioImpl
from app.infraestructura.repositorios.examen_repositorio_impl import ExamenRepositorioImpl
from app.infraestructura.repositorios.respuesta_estudiante_repositorio_impl import (
    RespuestaEstudianteRepositorioImpl,
)
from app.infraestructura.repositorios.perfil_academico_repositorio_impl import (
    PerfilAcademicoRepositorioImpl,
)
from app.infraestructura.repositorios.reporte_institucional_repositorio_impl import (
    ReporteInstitucionalRepositorioImpl,
)
from app.infraestructura.repositorios.ranking_repositorio_impl import (
    EntradaRankingRepositorioImpl,
)


def usuario_app_service() -> UsuarioAppService:
    return UsuarioAppService(UsuarioRepositorioImpl())


def examen_app_service() -> ExamenAppService:
    return ExamenAppService(ExamenRepositorioImpl())


def respuesta_estudiante_app_service() -> RespuestaEstudianteAppService:
    return RespuestaEstudianteAppService(
        RespuestaEstudianteRepositorioImpl(), ExamenRepositorioImpl()
    )


def perfil_academico_app_service() -> PerfilAcademicoAppService:
    return PerfilAcademicoAppService(
        PerfilAcademicoRepositorioImpl(), RespuestaEstudianteRepositorioImpl()
    )


def reporte_institucional_app_service() -> ReporteInstitucionalAppService:
    return ReporteInstitucionalAppService(
        ReporteInstitucionalRepositorioImpl(),
        RespuestaEstudianteRepositorioImpl(),
        ExamenRepositorioImpl(),
    )


def ranking_app_service() -> RankingAppService:
    return RankingAppService(EntradaRankingRepositorioImpl(), RespuestaEstudianteRepositorioImpl())
