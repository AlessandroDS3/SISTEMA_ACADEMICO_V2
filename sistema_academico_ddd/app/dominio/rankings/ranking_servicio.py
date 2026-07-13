"""Domain Service RankingServicio: construye el ranking de un Examen a
partir de las Calificaciones de sus RespuestaEstudiante.
"""
from typing import List

from app.dominio.calificacion_automatica.respuesta_estudiante import RespuestaEstudiante
from app.dominio.rankings.entrada_ranking import EntradaRanking


class RankingServicio:

    @staticmethod
    def construir_ranking(
        examen_id: int, respuestas: List[RespuestaEstudiante]
    ) -> List[EntradaRanking]:
        calificadas = [r for r in respuestas if r.calificacion is not None]
        ordenadas = sorted(calificadas, key=lambda r: r.calificacion.nota_final, reverse=True)

        return [
            EntradaRanking(
                examen_id=examen_id,
                estudiante_id=respuesta.estudiante_id,
                posicion=posicion,
                nota_final=respuesta.calificacion.nota_final,
            )
            for posicion, respuesta in enumerate(ordenadas, start=1)
        ]
