"""Servicio de infraestructura ProcesadorImagenServicio.

Fachada (Facade) sobre los modulos de vision por computadora
(document_scanner, corner_detector, orientacion, identificacion,
hoja_respuestas) migrados desde el proyecto de escritorio original.
Estos modulos NO tienen dependencias de Flask/SQLAlchemy: son
utilidades puras de OpenCV/NumPy, por lo que encajan naturalmente en
la capa de Infraestructura (acceso a un "servicio externo": la
libreria de vision por computadora) segun DDD.

Estilos de programacion ya presentes en este subdominio (no hace falta
reescribirlos, se documentan con su fragmento real en el README):
  - Pipeline: `identificacion.py` encadena
    `load_and_preprocess_image -> extract_id_section ->
    detect_filled_bubbles_in_dni`, cada funcion tomando la salida de la
    anterior.
  - Things: `ProcesadorExamenOMR` (`hoja_respuestas.py`) es un objeto
    con estado propio (umbrales, radios de busqueda) y comportamiento
    sobre ese estado (`procesar_completo`,
    `obtener_respuestas_detectadas`).

Esta fachada agrega dos estilos mas, a proposito en el punto de entrada
(no en el algoritmo numerico de OpenCV, que es sensible y no tiene
pruebas con imagenes reales): Cookbook (`procesar_hoja_completa`) y
Error/Exception Handling (`ImagenNoEncontradaError`).
"""
import os
from typing import Dict, List, Tuple

from app.infraestructura.procesamiento_imagen.document_scanner import ProcesadorDocumentos
from app.infraestructura.procesamiento_imagen.corner_detector import detectar_con_respaldo
from app.infraestructura.procesamiento_imagen.identificacion import process_answer_sheet
from app.infraestructura.procesamiento_imagen.hoja_respuestas import ProcesadorExamenOMR
from app.infraestructura.procesamiento_imagen.excepciones import ImagenNoEncontradaError


class ProcesadorImagenServicio:
    """Punto de entrada unico usado por la capa de Aplicacion para
    escanear y calificar una hoja de respuestas a partir de una imagen.
    """

    def __init__(self) -> None:
        self._procesador_documentos = ProcesadorDocumentos()

    def procesar_hoja_completa(self, ruta_imagen: str) -> Dict[str, str]:
        """Estilo Cookbook: se lee como una receta -- validar la imagen
        de entrada, escanear y corregir perspectiva, y extraer las
        respuestas marcadas -- en vez de que el llamador tenga que
        conocer y encadenar el orden correcto de los 3 pasos."""
        self._validar_que_la_imagen_existe(ruta_imagen)
        ruta_corregida = self.escanear_y_corregir_perspectiva(ruta_imagen)
        return self.extraer_respuestas_marcadas(ruta_corregida)

    def _validar_que_la_imagen_existe(self, ruta_imagen: str) -> None:
        """Estilo Error/Exception Handling: se valida temprano, en la
        fachada, en vez de dejar que el error de archivo faltante
        aparezca varios niveles adentro como una excepcion generica de
        OpenCV/NumPy dificil de asociar con la causa real."""
        if not os.path.isfile(ruta_imagen):
            raise ImagenNoEncontradaError(ruta_imagen)

    def escanear_y_corregir_perspectiva(self, ruta_imagen: str) -> str:
        """Detecta los bordes de la hoja de examen y corrige perspectiva.
        Devuelve la ruta de la imagen ya corregida.
        """
        resultado = detectar_con_respaldo(ruta_imagen, guardar_resultado=True)
        return resultado

    def identificar_estudiante(self, ruta_imagen_corregida: str) -> Tuple[List[int], str]:
        """Extrae el codigo del estudiante (burbujas de DNI/codigo) y el
        area de aplicacion marcada en la hoja."""
        return process_answer_sheet(ruta_imagen_corregida)

    def extraer_respuestas_marcadas(self, ruta_imagen_corregida: str) -> Dict[str, str]:
        """Detecta las alternativas marcadas (A/B/C/D) pregunta por
        pregunta usando el procesador OMR y las devuelve como
        {"1": "A", "2": "C", ...} listo para `RespuestaEstudiante`."""
        procesador_omr = ProcesadorExamenOMR(ruta_imagen_corregida)
        procesador_omr.procesar_completo()
        detectadas = procesador_omr.obtener_respuestas_detectadas()
        return {
            str(numero_pregunta): alternativa
            for numero_pregunta, alternativa, _estado in detectadas
            if alternativa is not None
        }
