"""Application Service: casos de uso de Reportes_y_Estadisticas
(generar reporte institucional consolidado de un Examen)."""
import statistics
from typing import List, Optional

from app.extensions import db
from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional
from app.dominio.reportes_estadisticas.reporte_institucional_repositorio import (
    IReporteInstitucionalRepositorio,
)
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)
from app.dominio.gestion_examenes.asignacion_grupo import AsignacionGrupo
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio
from app.dominio.gestion_examenes.excepciones import ExamenNoEncontradoError

NOTA_MINIMA_APROBATORIA = 11


class ReporteInstitucionalAppService:

    def __init__(
        self,
        reporte_repositorio: IReporteInstitucionalRepositorio,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
        examen_repositorio: IExamenRepositorio,
    ):
        self._reporte_repositorio = reporte_repositorio
        self._respuesta_repositorio = respuesta_repositorio
        self._examen_repositorio = examen_repositorio

    def generar_reporte(self, examen_id: int) -> ReporteInstitucional:
        """Caso de uso: 'Generar reporte institucional de un examen'."""
        self._validar_examen_existe(examen_id)

        respuestas = self._respuesta_repositorio.buscar_por_examen(examen_id)
        notas = [r.calificacion.nota_final for r in respuestas if r.calificacion is not None]

        promedio = statistics.mean(notas) if notas else 0.0
        desviacion = statistics.pstdev(notas) if len(notas) > 1 else 0.0

        reporte = ReporteInstitucional(
            examen_id=examen_id, promedio_general=promedio, desviacion_estandar=desviacion
        )

        aprobados, desaprobados = self._respuesta_repositorio.contar_por_umbral_nota(
            examen_id, NOTA_MINIMA_APROBATORIA
        )
        asignaciones = db.session.query(AsignacionGrupo).filter_by(examen_id=examen_id).all()
        for asignacion in asignaciones:
            reporte.registrar_estadistica_grupo(
                asignacion_grupo_id=asignacion.id,
                promedio_grupo=promedio,
                numero_aprobados=aprobados,
                numero_desaprobados=desaprobados,
            )

        return self._reporte_repositorio.guardar(reporte)

    def _validar_examen_existe(self, examen_id: int) -> None:
        """Estilo Error/Exception Handling: se reutiliza la misma
        excepcion de dominio `ExamenNoEncontradoError` que usa
        Gestion_de_Examenes, para que el error signifique lo mismo en
        todo el sistema en vez de que cada subdominio invente su propio
        "examen no encontrado"."""
        if self._examen_repositorio.buscar_por_id(examen_id) is None:
            raise ExamenNoEncontradoError(examen_id)

    def obtener_por_id(self, id: int) -> Optional[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_id(id)

    def listar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_examen(examen_id)
