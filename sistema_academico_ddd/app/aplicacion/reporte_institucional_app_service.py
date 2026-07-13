"""Application Service: casos de uso de Reportes_y_Estadisticas
(generar reporte institucional consolidado de un Examen)."""
import statistics
from typing import List, Optional

from app.extensions import db
from app.dominio.reportes_estadisticas.reporte_institucional import ReporteInstitucional
from app.dominio.reportes_estadisticas.estadistica_grupal import EstadisticaGrupal
from app.dominio.reportes_estadisticas.reporte_institucional_repositorio import (
    IReporteInstitucionalRepositorio,
)
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)
from app.dominio.gestion_examenes.asignacion_grupo import AsignacionGrupo


class ReporteInstitucionalAppService:

    def __init__(
        self,
        reporte_repositorio: IReporteInstitucionalRepositorio,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
    ):
        self._reporte_repositorio = reporte_repositorio
        self._respuesta_repositorio = respuesta_repositorio

    def generar_reporte(self, examen_id: int) -> ReporteInstitucional:
        """Caso de uso: 'Generar reporte institucional de un examen'."""
        respuestas = self._respuesta_repositorio.buscar_por_examen(examen_id)
        notas = [r.calificacion.nota_final for r in respuestas if r.calificacion is not None]

        promedio = statistics.mean(notas) if notas else 0.0
        desviacion = statistics.pstdev(notas) if len(notas) > 1 else 0.0

        reporte = ReporteInstitucional(
            examen_id=examen_id, promedio_general=promedio, desviacion_estandar=desviacion
        )
        reporte = self._reporte_repositorio.guardar(reporte)

        asignaciones = db.session.query(AsignacionGrupo).filter_by(examen_id=examen_id).all()
        for asignacion in asignaciones:
            estadistica = EstadisticaGrupal(
                reporte_id=reporte.id,
                asignacion_grupo_id=asignacion.id,
                promedio_grupo=promedio,
                numero_aprobados=sum(1 for n in notas if n >= 11),
                numero_desaprobados=sum(1 for n in notas if n < 11),
            )
            db.session.add(estadistica)
        db.session.commit()

        return reporte

    def obtener_por_id(self, id: int) -> Optional[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_id(id)

    def listar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_examen(examen_id)
