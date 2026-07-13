"""Application Service: casos de uso relacionados a Examen (creacion,
configuracion, banco de preguntas, asignacion a grupos)."""
from typing import List, Optional

from app.dominio.gestion_examenes.examen import Examen
from app.dominio.gestion_examenes.examen_factory import ExamenFactory
from app.dominio.gestion_examenes.examen_repositorio import IExamenRepositorio
from app.dominio.gestion_examenes.pregunta_banco import PreguntaBanco
from app.dominio.gestion_examenes.asignacion_grupo import AsignacionGrupo
from app.extensions import db


class ExamenAppService:

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
        examen = ExamenFactory.crear(
            titulo=titulo,
            materia_id=materia_id,
            creado_por_id=creado_por_id,
            numero_preguntas=numero_preguntas,
            numero_alternativas=numero_alternativas,
            puntaje_por_pregunta=puntaje_por_pregunta,
            penalizacion_por_error=penalizacion_por_error,
        )
        return self._repositorio.guardar(examen)

    def agregar_pregunta_al_banco(
        self, examen_id: int, numero_pregunta: int, respuesta_correcta: str, enunciado: str = ""
    ) -> PreguntaBanco:
        pregunta = PreguntaBanco(
            examen_id=examen_id,
            numero_pregunta=numero_pregunta,
            respuesta_correcta=respuesta_correcta,
            enunciado=enunciado,
        )
        db.session.add(pregunta)
        db.session.commit()
        return pregunta

    def asignar_grupo(self, examen_id: int, nombre_grupo: str, docente_id: int) -> AsignacionGrupo:
        asignacion = AsignacionGrupo(examen_id=examen_id, nombre_grupo=nombre_grupo, docente_id=docente_id)
        db.session.add(asignacion)
        db.session.commit()
        return asignacion

    def obtener_por_id(self, id: int) -> Optional[Examen]:
        return self._repositorio.buscar_por_id(id)

    def listar_por_materia(self, materia_id: int) -> List[Examen]:
        return self._repositorio.buscar_por_materia(materia_id)

    def listar_examenes(self) -> List[Examen]:
        return self._repositorio.listar()

    def actualizar_examen(
        self,
        id: int,
        titulo: str,
        materia_id: int,
        numero_preguntas: int,
        numero_alternativas: int = 4,
        puntaje_por_pregunta: float = 1.0,
    ) -> Examen:
        examen = self._repositorio.buscar_por_id(id)
        if examen is None:
            raise ValueError(f"No existe un examen con id {id}")

        examen.titulo = titulo
        examen.materia_id = materia_id
        examen.numero_preguntas = numero_preguntas
        if examen.configuracion is not None:
            examen.configuracion.numero_alternativas = numero_alternativas
            examen.configuracion.puntaje_por_pregunta = puntaje_por_pregunta
        return self._repositorio.actualizar(examen)

    def eliminar_examen(self, id: int) -> bool:
        return self._repositorio.eliminar(id)
