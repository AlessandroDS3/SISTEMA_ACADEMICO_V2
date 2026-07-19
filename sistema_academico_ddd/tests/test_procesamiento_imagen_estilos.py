"""Pruebas del estilo Error/Exception Handling agregado en Lab 10 sobre
la fachada ProcesadorImagenServicio: valida la imagen de entrada antes
de tocar OpenCV. (Pipeline y Things ya estaban presentes en este
subdominio -- ver `identificacion.py` y `hoja_respuestas.py`,
documentados con su propio fragmento en el README)."""
import pytest

from app.infraestructura.procesamiento_imagen.procesador_imagen_servicio import (
    ProcesadorImagenServicio,
)
from app.infraestructura.procesamiento_imagen.excepciones import ImagenNoEncontradaError


def test_procesar_hoja_completa_con_ruta_inexistente_lanza_excepcion_de_dominio():
    servicio = ProcesadorImagenServicio()

    with pytest.raises(ImagenNoEncontradaError):
        servicio.procesar_hoja_completa("esta/ruta/no/existe.jpg")
