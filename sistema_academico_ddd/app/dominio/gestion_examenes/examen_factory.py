"""Factory de dominio para construir un Examen junto a su
ConfiguracionExamen por defecto (UMLClass ExamenFactory).
"""
from typing import Optional

from app.dominio.gestion_examenes.examen import Examen
from app.dominio.gestion_examenes.configuracion_examen import ConfiguracionExamen


class ExamenFactory:

    @staticmethod
    def crear(
        titulo: str,
        materia_id: int,
        creado_por_id: int,
        numero_preguntas: int,
        numero_alternativas: int = 4,
        puntaje_por_pregunta: float = 1.0,
        penalizacion_por_error: float = 0.0,
        tiempo_limite_minutos: Optional[int] = None,
    ) -> Examen:
        examen = Examen(
            titulo=titulo,
            materia_id=materia_id,
            creado_por_id=creado_por_id,
            numero_preguntas=numero_preguntas,
        )
        examen.configuracion = ConfiguracionExamen(
            numero_alternativas=numero_alternativas,
            puntaje_por_pregunta=puntaje_por_pregunta,
            penalizacion_por_error=penalizacion_por_error,
            tiempo_limite_minutos=tiempo_limite_minutos,
        )
        return examen
