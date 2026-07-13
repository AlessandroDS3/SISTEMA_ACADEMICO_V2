"""Servicio de infraestructura: procesamiento de imagen (OMR).

Modulos migrados desde el proyecto de escritorio original
(00000_PROCESADOR_IMAGEN):
  - document_scanner.py   -> deteccion/mejora de documentos (OpenCV)
  - corner_detector.py    -> deteccion de esquinas y correccion de perspectiva
  - orientacion.py        -> correccion de orientacion por bordes
  - identificacion.py     -> lectura de codigo de estudiante / area
  - hoja_respuestas.py    -> lectura de burbujas marcadas (antes respuestas.py)

`ProcesadorImagenServicio` es la fachada que la capa de Aplicacion debe
usar; los demas modulos son detalle interno de infraestructura.
"""
from app.infraestructura.procesamiento_imagen.procesador_imagen_servicio import (
    ProcesadorImagenServicio,
)

__all__ = ["ProcesadorImagenServicio"]
