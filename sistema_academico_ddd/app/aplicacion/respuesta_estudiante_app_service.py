"""Application Service: caso de uso principal del sistema -- procesar
la hoja de examen escaneada de un estudiante y calificarla
automaticamente.

Orquesta 3 piezas:
  1. Infraestructura: ProcesadorImagenServicio (OMR, ex-Flet app)
  2. Dominio: CalificacionServicio (regla de negocio de calificacion)
  3. Repositorios: persistencia de RespuestaEstudiante y Calificacion
"""
from typing import Callable, Dict, List, Optional

from app.extensions import db
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion_servicio import CalificacionServicio
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio
from app.dominio.gestion_examenes.excepciones import ExamenNoEncontradoError
from app.infraestructura.procesamiento_imagen.procesador_imagen_servicio import (
    ProcesadorImagenServicio,
)


class RespuestaEstudianteAppService:
    """`procesar_hoja_escaneada` sigue el estilo Pipeline: el caso de
    uso se modela como una tuberia de etapas (`_ETAPAS`), cada una
    recibe el `contexto` que dejo la etapa anterior, le agrega su
    propio resultado y lo devuelve para la siguiente -- el dato "fluye"
    de principio a fin en vez de vivir en variables locales sueltas
    dentro de un unico metodo largo."""

    def __init__(
        self,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
        examen_repositorio: IExamenRepositorio,
        procesador_imagen: Optional[ProcesadorImagenServicio] = None,
    ):
        self._respuesta_repositorio = respuesta_repositorio
        self._examen_repositorio = examen_repositorio
        self._procesador_imagen = procesador_imagen or ProcesadorImagenServicio()
        self._ETAPAS: List[Callable[[Dict], Dict]] = [
            self._etapa_obtener_examen,
            self._etapa_escanear_y_corregir,
            self._etapa_extraer_respuestas_marcadas,
            self._etapa_guardar_respuesta,
            self._etapa_calificar_y_guardar,
        ]

    def procesar_hoja_escaneada(
        self, examen_id: int, estudiante_id: int, ruta_imagen: str
    ) -> RespuestaEstudiante:
        """Caso de uso: 'Calificar hoja de examen escaneada'."""
        contexto = {
            "examen_id": examen_id,
            "estudiante_id": estudiante_id,
            "ruta_imagen": ruta_imagen,
        }
        for etapa in self._ETAPAS:
            contexto = etapa(contexto)
        return contexto["respuesta"]

    def _etapa_obtener_examen(self, contexto: Dict) -> Dict:
        examen = self._examen_repositorio.buscar_por_id(contexto["examen_id"])
        if examen is None:
            raise ExamenNoEncontradoError(contexto["examen_id"])
        contexto["examen"] = examen
        return contexto

    def _etapa_escanear_y_corregir(self, contexto: Dict) -> Dict:
        contexto["ruta_corregida"] = self._procesador_imagen.escanear_y_corregir_perspectiva(
            contexto["ruta_imagen"]
        )
        return contexto

    def _etapa_extraer_respuestas_marcadas(self, contexto: Dict) -> Dict:
        contexto["respuestas_marcadas"] = self._procesador_imagen.extraer_respuestas_marcadas(
            contexto["ruta_corregida"]
        )
        return contexto

    def _etapa_guardar_respuesta(self, contexto: Dict) -> Dict:
        respuesta = RespuestaEstudiante(
            examen_id=contexto["examen_id"],
            estudiante_id=contexto["estudiante_id"],
            respuestas_marcadas=contexto["respuestas_marcadas"],
            ruta_imagen_original=contexto["ruta_imagen"],
        )
        contexto["respuesta"] = self._respuesta_repositorio.guardar(respuesta)
        return contexto

    def _etapa_calificar_y_guardar(self, contexto: Dict) -> Dict:
        examen = contexto["examen"]
        calificacion = CalificacionServicio.calificar(
            contexto["respuesta"], examen.preguntas, examen.configuracion
        )
        db.session.add(calificacion)
        db.session.commit()
        return contexto

    def obtener_por_id(self, id: int) -> Optional[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_id(id)

    def listar_por_examen(self, examen_id: int) -> List[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_examen(examen_id)

    def listar_por_estudiante(self, estudiante_id: int) -> List[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_estudiante(estudiante_id)
