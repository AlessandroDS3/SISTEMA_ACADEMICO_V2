"""Application Service: caso de uso principal del sistema -- procesar
la hoja de examen escaneada de un estudiante y calificarla
automaticamente.

Orquesta 3 piezas:
  1. Infraestructura: ProcesadorImagenServicio (OMR, ex-Flet app)
  2. Dominio: CalificacionServicio (regla de negocio de calificacion)
  3. Repositorios: persistencia de RespuestaEstudiante y Calificacion
"""
from typing import List, Optional

from app.extensions import db
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion_servicio import CalificacionServicio
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio
from app.infraestructura.procesamiento_imagen.procesador_imagen_servicio import (
    ProcesadorImagenServicio,
)


class RespuestaEstudianteAppService:

    def __init__(
        self,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
        examen_repositorio: IExamenRepositorio,
        procesador_imagen: Optional[ProcesadorImagenServicio] = None,
    ):
        self._respuesta_repositorio = respuesta_repositorio
        self._examen_repositorio = examen_repositorio
        self._procesador_imagen = procesador_imagen or ProcesadorImagenServicio()

    def procesar_hoja_escaneada(
        self, examen_id: int, estudiante_id: int, ruta_imagen: str
    ) -> RespuestaEstudiante:
        """Caso de uso: 'Calificar hoja de examen escaneada'."""
        examen = self._examen_repositorio.buscar_por_id(examen_id)
        if examen is None:
            raise ValueError(f"Examen {examen_id} no existe")

        ruta_corregida = self._procesador_imagen.escanear_y_corregir_perspectiva(ruta_imagen)
        respuestas_marcadas = self._procesador_imagen.extraer_respuestas_marcadas(ruta_corregida)

        respuesta = RespuestaEstudiante(
            examen_id=examen_id,
            estudiante_id=estudiante_id,
            respuestas_marcadas=respuestas_marcadas,
            ruta_imagen_original=ruta_imagen,
        )
        respuesta = self._respuesta_repositorio.guardar(respuesta)

        calificacion = CalificacionServicio.calificar(
            respuesta, examen.preguntas, examen.configuracion
        )
        db.session.add(calificacion)
        db.session.commit()

        return respuesta

    def obtener_por_id(self, id: int) -> Optional[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_id(id)

    def listar_por_examen(self, examen_id: int) -> List[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_examen(examen_id)

    def listar_por_estudiante(self, estudiante_id: int) -> List[RespuestaEstudiante]:
        return self._respuesta_repositorio.buscar_por_estudiante(estudiante_id)
