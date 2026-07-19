"""Application Service: casos de uso relacionados a Examen (creacion,
configuracion, banco de preguntas, asignacion a grupos)."""
from typing import List, Optional

from app.dominio.gestion_examenes.examen import Examen
from app.dominio.gestion_examenes.examen_factory import ExamenFactory
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio
from app.dominio.gestion_examenes.pregunta_banco import PreguntaBanco
from app.dominio.gestion_examenes.asignacion_grupo import AsignacionGrupo
from app.dominio.gestion_examenes.excepciones import (
    ExamenNoEncontradoError,
    NumeroPreguntasInvalidoError,
)
from app.extensions import db


class ExamenAppService:
    """Casos de uso de examenes.

    `crear_examen` y `actualizar_examen` siguen el estilo Cookbook: cada
    uno es una "receta" que se lee como un indice de pasos con nombre
    propio (`_validar_...`, `_construir_...`, `_persistir_...`), en vez
    de una sola funcion larga que mezcle validacion, construccion y
    persistencia en el mismo bloque.
    """

    def __init__(self, examen_repositorio: IExamenRepositorio):
        self._repositorio = examen_repositorio

    def crear_examen(
        self,
        titulo: str,
        materia_id: int,
        creado_por_id: int,
        numero_preguntas: int,
        numero_alternativas: int = 4,
        puntaje_por_pregunta: float = 1.0,
        penalizacion_por_error: float = 0.0,
    ) -> Examen:
        self._validar_numero_preguntas(numero_preguntas)
        examen = self._construir_examen_con_configuracion(
            titulo,
            materia_id,
            creado_por_id,
            numero_preguntas,
            numero_alternativas,
            puntaje_por_pregunta,
            penalizacion_por_error,
        )
        return self._persistir_examen_nuevo(examen)

    def _validar_numero_preguntas(self, numero_preguntas: int) -> None:
        if numero_preguntas <= 0:
            raise NumeroPreguntasInvalidoError(numero_preguntas)

    def _construir_examen_con_configuracion(
        self,
        titulo: str,
        materia_id: int,
        creado_por_id: int,
        numero_preguntas: int,
        numero_alternativas: int,
        puntaje_por_pregunta: float,
        penalizacion_por_error: float,
    ) -> Examen:
        return ExamenFactory.crear(
            titulo=titulo,
            materia_id=materia_id,
            creado_por_id=creado_por_id,
            numero_preguntas=numero_preguntas,
            numero_alternativas=numero_alternativas,
            puntaje_por_pregunta=puntaje_por_pregunta,
            penalizacion_por_error=penalizacion_por_error,
        )

    def _persistir_examen_nuevo(self, examen: Examen) -> Examen:
        return self._repositorio.guardar(examen)

    def agregar_pregunta_al_banco(
        self, examen_id: int, numero_pregunta: int, respuesta_correcta: str, enunciado: str = ""
    ) -> PreguntaBanco:
        examen = self._buscar_examen_existente(examen_id)
        pregunta = PreguntaBanco(
            numero_pregunta=numero_pregunta,
            respuesta_correcta=respuesta_correcta,
            enunciado=enunciado,
        )
        examen.agregar_pregunta(pregunta)
        db.session.commit()
        return pregunta

    def asignar_grupo(self, examen_id: int, nombre_grupo: str, docente_id: int) -> AsignacionGrupo:
        asignacion = AsignacionGrupo(examen_id=examen_id, nombre_grupo=nombre_grupo, docente_id=docente_id)
        db.session.add(asignacion)
        db.session.commit()
        return asignacion

    def obtener_por_id(self, examen_id: int) -> Optional[Examen]:
        return self._repositorio.buscar_por_id(examen_id)

    def listar_por_materia(self, materia_id: int) -> List[Examen]:
        return self._repositorio.buscar_por_materia(materia_id)

    def listar_examenes(self) -> List[Examen]:
        return self._repositorio.listar()

    def actualizar_examen(
        self,
        examen_id: int,
        titulo: str,
        materia_id: int,
        numero_preguntas: int,
        numero_alternativas: int = 4,
        puntaje_por_pregunta: float = 1.0,
    ) -> Examen:
        examen = self._buscar_examen_existente(examen_id)
        self._aplicar_cambios_basicos(examen, titulo, materia_id, numero_preguntas)
        self._aplicar_cambios_configuracion(examen, numero_alternativas, puntaje_por_pregunta)
        return self._repositorio.actualizar(examen)

    def _buscar_examen_existente(self, examen_id: int) -> Examen:
        examen = self._repositorio.buscar_por_id(examen_id)
        if examen is None:
            raise ExamenNoEncontradoError(examen_id)
        return examen

    def _aplicar_cambios_basicos(
        self, examen: Examen, titulo: str, materia_id: int, numero_preguntas: int
    ) -> None:
        examen.titulo = titulo
        examen.materia_id = materia_id
        examen.numero_preguntas = numero_preguntas

    def _aplicar_cambios_configuracion(
        self, examen: Examen, numero_alternativas: int, puntaje_por_pregunta: float
    ) -> None:
        if examen.configuracion is not None:
            examen.configuracion.numero_alternativas = numero_alternativas
            examen.configuracion.puntaje_por_pregunta = puntaje_por_pregunta

    def eliminar_examen(self, examen_id: int) -> bool:
        return self._repositorio.eliminar(examen_id)
