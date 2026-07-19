"""Implementacion concreta de IEntradaRankingRepositorio usando SQLAlchemy."""
from typing import Iterator, List

from app.extensions import db
from app.dominio.rankings.entrada_ranking import EntradaRanking
from app.dominio.rankings.ranking_repositorio import IEntradaRankingRepositorio


class EntradaRankingRepositorioImpl(IEntradaRankingRepositorio):

    def guardar_todas(self, entradas: List[EntradaRanking]) -> List[EntradaRanking]:
        db.session.add_all(entradas)
        db.session.commit()
        return entradas

    def top_n_por_examen(self, examen_id: int, n: int) -> List[EntradaRanking]:
        """Estilo Persistent-Tables: pedimos a la base de datos las `n`
        mejores posiciones ya ordenadas (`ORDER BY ... LIMIT n`), en vez
        de traer TODAS las entradas del examen y recortarlas en Python
        con `sorted(...)[:n]`."""
        return (
            db.session.query(EntradaRanking)
            .filter_by(examen_id=examen_id)
            .order_by(EntradaRanking.posicion.asc())
            .limit(n)
            .all()
        )

    def iterar_por_examen(self, examen_id: int) -> Iterator[EntradaRanking]:
        """Estilo Lazy-Rivers: un generador que va trayendo filas de la
        base de datos en lotes (`yield_per`) a medida que el llamador
        las consume, en vez de cargar el ranking completo del examen
        (que puede ser de miles de estudiantes) en una lista antes de
        poder iterarlo."""
        consulta = (
            db.session.query(EntradaRanking)
            .filter_by(examen_id=examen_id)
            .order_by(EntradaRanking.posicion.asc())
            .yield_per(50)
        )
        for entrada in consulta:
            yield entrada
