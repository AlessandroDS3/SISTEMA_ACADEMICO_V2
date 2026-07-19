"""Estilo Trinity aplicado al recalculo del promedio general de un
PerfilAcademico tras un nuevo examen.

El estilo Trinity separa un mismo concepto en tres piezas que
colaboran pero tienen una unica responsabilidad cada una:
  - `EvolucionAcademicaEstado`: solo GUARDA una referencia al estado
    (el PerfilAcademico y la nota nueva). No sabe leerlo ni escribirlo.
  - `EvolucionAcademicaLector`: solo LEE el estado para producir un
    dato derivado (la lista de notas historicas + la nueva).
  - `EvolucionAcademicaEscritor`: solo ESCRIBE el estado (aplica el
    promedio ya calculado). Nunca decide nada a partir de una lectura.

Esto evita que una sola clase/metodo mezcle "leer todo, decidir y
escribir" en el mismo lugar.
"""
from typing import List

from app.dominio.seguimiento_academico.perfil_academico import PerfilAcademico


class EvolucionAcademicaEstado:
    def __init__(self, perfil: PerfilAcademico, nota_nueva: float):
        self.perfil = perfil
        self.nota_nueva = nota_nueva


class EvolucionAcademicaLector:
    @staticmethod
    def notas_historicas(estado: EvolucionAcademicaEstado) -> List[float]:
        return [e.nota_final for e in estado.perfil.evoluciones_nota] + [estado.nota_nueva]


class EvolucionAcademicaEscritor:
    @staticmethod
    def aplicar_nuevo_promedio(estado: EvolucionAcademicaEstado, notas: List[float]) -> None:
        estado.perfil.promedio_general = sum(notas) / len(notas)
