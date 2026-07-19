"""Application Service: casos de uso del subdominio Rankings (generar
y consultar el ranking de un Examen a partir de las Calificaciones de
sus RespuestaEstudiante)."""
from typing import Iterator, List

from app.dominio.rankings.entrada_ranking import EntradaRanking
from app.dominio.rankings.ranking_servicio import RankingServicio
from app.dominio.rankings.ranking_repositorio import IEntradaRankingRepositorio
from app.dominio.calificacion_automatica.respuesta_estudiante_repositorio import (
    IRespuestaEstudianteRepositorio,
)


class RankingAppService:

    def __init__(
        self,
        ranking_repositorio: IEntradaRankingRepositorio,
        respuesta_repositorio: IRespuestaEstudianteRepositorio,
    ):
        self._ranking_repositorio = ranking_repositorio
        self._respuesta_repositorio = respuesta_repositorio

    def generar_ranking(self, examen_id: int) -> List[EntradaRanking]:
        """Caso de uso: 'Generar ranking de un examen'."""
        respuestas = self._respuesta_repositorio.buscar_por_examen(examen_id)
        entradas = RankingServicio.construir_ranking(examen_id, respuestas)
        return self._ranking_repositorio.guardar_todas(entradas)

    def obtener_top(self, examen_id: int, n: int = 10) -> List[EntradaRanking]:
        return self._ranking_repositorio.top_n_por_examen(examen_id, n)

    def iterar_ranking_completo(self, examen_id: int) -> Iterator[EntradaRanking]:
        return self._ranking_repositorio.iterar_por_examen(examen_id)
