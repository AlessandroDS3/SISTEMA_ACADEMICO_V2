"""Application Service: casos de uso de Reportes_y_Estadisticas
(generar reporte institucional consolidado de un Examen)."""
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
        """Caso de uso: 'Generar reporte institucional de un examen'.

        Estilo Cookbook: el caso de uso se lee como una receta de pasos
        con nombre propio; cada paso esta extraido en su propio metodo y
        el cuerpo describe *que* se hace, no *como*.
        """
        self._validar_examen_existe(examen_id)
        reporte = self._construir_reporte_con_estadisticas(examen_id)
        self._registrar_estadisticas_por_grupo(reporte, examen_id)
        return self._persistir_reporte(reporte)

    def _construir_reporte_con_estadisticas(self, examen_id: int) -> ReporteInstitucional:
        """Paso 2 de la receta: pedir al repositorio el promedio y la
        desviacion ya agregados en SQL (estilo Persistent-Tables)."""
        promedio, desviacion = self._reporte_repositorio.estadisticas_nota_por_examen(examen_id)
        return ReporteInstitucional(
            examen_id=examen_id, promedio_general=promedio, desviacion_estandar=desviacion
        )

    def _registrar_estadisticas_por_grupo(
        self, reporte: ReporteInstitucional, examen_id: int
    ) -> None:
        """Paso 3 de la receta: delegar en la entidad el registro de una
        estadistica por cada grupo asignado al examen (estilo Things)."""
        aprobados, desaprobados = self._respuesta_repositorio.contar_por_umbral_nota(
            examen_id, NOTA_MINIMA_APROBATORIA
        )
        asignaciones = db.session.query(AsignacionGrupo).filter_by(examen_id=examen_id).all()
        for asignacion in asignaciones:
            reporte.registrar_estadistica_grupo(
                asignacion_grupo_id=asignacion.id,
                promedio_grupo=reporte.promedio_general,
                numero_aprobados=aprobados,
                numero_desaprobados=desaprobados,
            )

    def _persistir_reporte(self, reporte: ReporteInstitucional) -> ReporteInstitucional:
        """Paso 4 de la receta: persistir el agregado ya construido."""
        return self._reporte_repositorio.guardar(reporte)

    def _validar_examen_existe(self, examen_id: int) -> None:
        """Estilo Error/Exception Handling: se reutiliza la misma
        excepcion de dominio `ExamenNoEncontradoError` que usa
        Gestion_de_Examenes, para que el error signifique lo mismo en
        todo el sistema en vez de que cada subdominio invente su propio
        "examen no encontrado"."""
        if self._examen_repositorio.buscar_por_id(examen_id) is None:
            raise ExamenNoEncontradoError(examen_id)

    def obtener_por_id(self, reporte_id: int) -> Optional[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_id(reporte_id)

    def listar_por_examen(self, examen_id: int) -> List[ReporteInstitucional]:
        return self._reporte_repositorio.buscar_por_examen(examen_id)
