"""Interfaz de repositorio del dominio (UMLInterface IEntradaRankingRepositorio)."""
from abc import ABC, abstractmethod
from typing import Iterator, List

from app.dominio.rankings.entrada_ranking import EntradaRanking


class IEntradaRankingRepositorio(ABC):

    @abstractmethod
    def guardar_todas(self, entradas: List[EntradaRanking]) -> List[EntradaRanking]:
        ...

    @abstractmethod
    def top_n_por_examen(self, examen_id: int, n: int) -> List[EntradaRanking]:
        """Estilo Persistent-Tables: el `ORDER BY` + `LIMIT` los aplica
        la base de datos, no un `sorted(...)[:n]` en Python."""
        ...

    @abstractmethod
    def iterar_por_examen(self, examen_id: int) -> Iterator[EntradaRanking]:
        """Estilo Lazy-Rivers: recorre el ranking completo de forma
        perezosa, sin materializar toda la tabla en memoria."""
        ...
