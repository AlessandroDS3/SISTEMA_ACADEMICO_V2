"""Servicio de infraestructura ProcesadorImagenServicio.

Fachada (Facade) sobre los modulos de vision por computadora
(document_scanner, corner_detector, orientacion, identificacion,
hoja_respuestas) migrados desde el proyecto de escritorio original.
Estos modulos NO tienen dependencias de Flask/SQLAlchemy: son
utilidades puras de OpenCV/NumPy, por lo que encajan naturalmente en
la capa de Infraestructura (acceso a un "servicio externo": la
libreria de vision por computadora) segun DDD.
"""
from typing import Dict, List, Tuple

from app.infraestructura.procesamiento_imagen.document_scanner import ProcesadorDocumentos
from app.infraestructura.procesamiento_imagen.corner_detector import detectar_con_respaldo
from app.infraestructura.procesamiento_imagen.orientacion import corregir_orientacion_por_bordes
from app.infraestructura.procesamiento_imagen.identificacion import procesar_hoja_respuestas
from app.infraestructura.procesamiento_imagen.hoja_respuestas import ProcesadorExamenOMR


class ProcesadorImagenServicio:
    """Punto de entrada unico usado por la capa de Aplicacion para
    escanear y calificar una hoja de respuestas a partir de una imagen.
    """

    def __init__(self) -> None:
        self._procesador_documentos = ProcesadorDocumentos()

    def escanear_y_corregir_perspectiva(self, ruta_imagen: str) -> str:
        """Detecta los bordes de la hoja de examen y corrige perspectiva.
        Devuelve la ruta de la imagen ya corregida.
        """
        resultado = detectar_con_respaldo(ruta_imagen, guardar_resultado=True)
        return resultado

    def identificar_estudiante(self, ruta_imagen_corregida: str) -> Tuple[List[int], str]:
        """Extrae el codigo del estudiante (burbujas de DNI/codigo) y el
        area de aplicacion marcada en la hoja."""
        return procesar_hoja_respuestas(ruta_imagen_corregida)

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
