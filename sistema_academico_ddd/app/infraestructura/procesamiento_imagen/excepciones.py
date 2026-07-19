"""Excepciones de infraestructura del procesamiento de imagen (OMR).

Estilo de programacion: Error/Exception Handling. Antes de este
cambio, si la ruta de la imagen no existia, el error de bajo nivel
llegaba envuelto en excepciones geneticas de OpenCV/NumPy (o incluso
en un `None` silencioso) varios niveles adentro del procesamiento. Se
valida temprano, en la fachada, con una excepcion de dominio propia y
un mensaje claro."""


class ProcesamientoImagenError(ValueError):
    """Raiz de las excepciones del procesamiento OMR."""


class ImagenNoEncontradaError(ProcesamientoImagenError):
    def __init__(self, ruta_imagen: str):
        super().__init__(f"No se encontro el archivo de imagen: {ruta_imagen}")
        self.ruta_imagen = ruta_imagen
