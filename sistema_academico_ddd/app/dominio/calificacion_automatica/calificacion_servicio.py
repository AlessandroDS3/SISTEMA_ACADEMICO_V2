"""Domain Service CalificacionServicio: encapsula la logica de negocio
para calificar una RespuestaEstudiante contra el banco de preguntas de
un Examen (UMLClass CalificacionServicio, stereotype <<service>>).
"""
from typing import List

from app.dominio.gestion_examenes.pregunta_banco import PreguntaBanco
from app.dominio.gestion_examenes.configuracion_examen import ConfiguracionExamen
from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.calificacion_automatica.calificacion import Calificacion


class CalificacionServicio:

    @staticmethod
    def calificar(
        respuesta: RespuestaEstudiante,
        preguntas: List[PreguntaBanco],
        configuracion: ConfiguracionExamen,
    ) -> Calificacion:
        correctas = incorrectas = en_blanco = 0
        marcadas = respuesta.respuestas_marcadas or {}

        for pregunta in preguntas:
            marcada = marcadas.get(str(pregunta.numero_pregunta))
            if not marcada:
                en_blanco += 1
            elif marcada.upper() == pregunta.respuesta_correcta.upper():
                correctas += 1
            else:
                incorrectas += 1

        return Calificacion.calcular(
            respuesta_id=respuesta.id,
            numero_correctas=correctas,
            numero_incorrectas=incorrectas,
            numero_en_blanco=en_blanco,
            puntaje_por_pregunta=configuracion.puntaje_por_pregunta,
            penalizacion_por_error=configuracion.penalizacion_por_error,
        )
