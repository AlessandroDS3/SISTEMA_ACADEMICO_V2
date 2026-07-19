"""Pruebas unitarias del subdominio Area_y_Materia: Things
(comportamiento encapsulado en Area) y Error/Exception Handling
(excepcion de dominio propia al violar el invariante)."""
import pytest

from app.dominio.area_materia.area import Area
from app.dominio.area_materia.materia import Materia
from app.dominio.area_materia.excepciones import MateriaDuplicadaError


def test_agregar_materia_la_asocia_al_area():
    area = Area(nombre="Ciencias")
    materia = Materia(nombre="Fisica", codigo="FIS101")

    area.agregar_materia(materia)

    assert materia in area.materias
    assert materia.area is area


def test_agregar_materia_con_codigo_repetido_lanza_excepcion_de_dominio():
    area = Area(nombre="Ciencias")
    area.agregar_materia(Materia(nombre="Fisica", codigo="FIS101"))

    with pytest.raises(MateriaDuplicadaError):
        area.agregar_materia(Materia(nombre="Fisica II", codigo="FIS101"))
