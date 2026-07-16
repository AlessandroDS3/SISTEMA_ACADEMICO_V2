import cv2
import numpy as np
from typing import Tuple, Optional, List
import logging
import sys

logger = logging.getLogger(__name__)

# Umbrales de luminosidad promedio (escala de grises 0-255) usados para
# clasificar un documento antes de elegir la estrategia de realce de contraste.
UMBRAL_LUMINOSIDAD_MUY_OSCURA = 120
UMBRAL_LUMINOSIDAD_OSCURA = 140
UMBRAL_LUMINOSIDAD_NORMAL = 165
UMBRAL_LUMINOSIDAD_CLARA = 200


class MejoradorDocumentos:
    """
    Clase para mejorar el contraste y saturación de documentos.
    """

    def mejorar_contraste_documentos(self, imagen: np.ndarray) -> np.ndarray:
        """
        Mejora el contraste de documentos según su luminosidad.
        """
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        promedio = np.mean(gris.astype(np.float32))

        if promedio <= UMBRAL_LUMINOSIDAD_MUY_OSCURA:
            tipo = "muy_oscura"
        elif promedio <= UMBRAL_LUMINOSIDAD_OSCURA:
            tipo = "oscura"
        elif promedio <= UMBRAL_LUMINOSIDAD_NORMAL:
            tipo = "normal"
        elif promedio <= UMBRAL_LUMINOSIDAD_CLARA:
            tipo = "clara"
        else:
            tipo = "muy_clara"

        if tipo == "muy_oscura":
            resultado = imagen
        elif tipo == "oscura":
            resultado = imagen
        elif tipo == "normal":
            resultado = cv2.convertScaleAbs(imagen, alpha=1.15, beta=10)
            imagen_lab = cv2.cvtColor(resultado, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(imagen_lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l_eq = clahe.apply(l)
            imagen_lab_mejorada = cv2.merge((l_eq, a, b))
            resultado = cv2.cvtColor(imagen_lab_mejorada, cv2.COLOR_LAB2BGR)
        elif tipo == "clara":
            imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(imagen_lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6,6))
            l_eq = clahe.apply(l)
            imagen_lab_mejorada = cv2.merge((l_eq, a, b))
            resultado = cv2.cvtColor(imagen_lab_mejorada, cv2.COLOR_LAB2BGR)
            resultado = cv2.convertScaleAbs(resultado, alpha=1.3, beta=15)
        elif tipo == "muy_clara":
            imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(imagen_lab)
            clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4,4))
            l_eq = clahe.apply(l)
            imagen_lab_mejorada = cv2.merge((l_eq, a, b))
            resultado = cv2.cvtColor(imagen_lab_mejorada, cv2.COLOR_LAB2BGR)
            resultado = cv2.convertScaleAbs(resultado, alpha=1.4, beta=20)
        
        return resultado

    def procesar_imagen_completa(self, imagen: np.ndarray) -> np.ndarray:
        """
        Procesa la imagen completa mejorando contraste y saturación.
        """
        imagen_contraste = self.mejorar_contraste_documentos(imagen)
        
        imagen_hsv = cv2.cvtColor(imagen_contraste, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imagen_hsv)
        s = (s.astype(np.float32) * 1.1).clip(0, 255).astype(np.uint8)
        imagen_hsv_mejorada = cv2.merge((h, s, v))
        imagen_final = cv2.cvtColor(imagen_hsv_mejorada, cv2.COLOR_HSV2BGR)
        
        return imagen_final


class DetectorDocumentosDual:
    def __init__(self, ratio_area_minima: float = 0.1, dimension_maxima: int = 1500, umbral_ruido: float = 10.0):
        """
        Detector de documentos dual que mantiene la resolución original.
        
        Args:
            ratio_area_minima: Ratio mínimo del área del documento respecto a la imagen
            dimension_maxima: Dimensión máxima para redimensionar SOLO para detección
            umbral_ruido: Umbral de ruido para aplicar filtro de suavizado
        """
        self.ratio_area_minima = ratio_area_minima
        self.dimension_maxima = dimension_maxima
        self.umbral_ruido = umbral_ruido
        self.mejorador = MejoradorDocumentos()
        
        # Configuraciones específicas para cada método
        self.configuracion_metodo1 = {
            'factor_epsilon': 0.02,
            'kernel_gaussiano': 3,
            'canny_bajo': 75,
            'canny_alto': 200
        }
        
        self.configuracion_metodo2 = {
            'factor_epsilon': 0.03,
            'kernel_gaussiano': 3,
            'canny_bajo': 0,
            'canny_alto': 50
        }
    
    def estimar_ruido_y_filtrar(self, imagen: np.ndarray) -> Tuple[np.ndarray, bool, float]:
        """
        Estima el ruido de la imagen y aplica filtro suave si es necesario.
        """
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        else:
            gris = imagen.copy()
        
        tamaño_roi = min(100, gris.shape[0] // 4, gris.shape[1] // 4)
        roi = gris[0:tamaño_roi, 0:tamaño_roi]
        
        nivel_ruido = np.std(roi.astype(np.float32))
        
        if nivel_ruido > self.umbral_ruido:
            if len(imagen.shape) == 3:
                imagen_filtrada = cv2.GaussianBlur(imagen, (3, 3), 0.5)
            else:
                imagen_filtrada = cv2.GaussianBlur(imagen, (3, 3), 0.5)
            
            return imagen_filtrada, True, float(nivel_ruido)
        
        return imagen.copy(), False, float(nivel_ruido)
    
    def redimensionar_solo_para_deteccion(self, imagen: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Redimensiona SOLO para detección, manteniendo la imagen original intacta.
        """
        altura, ancho = imagen.shape[:2]
        maximo_actual = max(altura, ancho)
        
        if maximo_actual <= self.dimension_maxima:
            return imagen.copy(), 1.0
        
        factor_escala = self.dimension_maxima / maximo_actual
        nuevo_ancho = int(ancho * factor_escala)
        nueva_altura = int(altura * factor_escala)
        
        redimensionada = cv2.resize(imagen, (nuevo_ancho, nueva_altura), interpolation=cv2.INTER_AREA)
        return redimensionada, factor_escala
    
    def escalar_contorno_a_original(self, contorno: np.ndarray, factor_escala: float) -> np.ndarray:
        """
        Escala un contorno de vuelta al tamaño original.
        """
        if factor_escala == 1.0:
            return contorno
        return (contorno / factor_escala).astype(np.int32)
    
    def ordenar_puntos_metodo1(self, puntos: np.ndarray) -> np.ndarray:
        """
        Ordena los puntos para transformación de perspectiva.
        """
        rectangulo = np.zeros((4, 2), dtype="float32")
        
        suma = puntos.sum(axis=1)
        rectangulo[0] = puntos[np.argmin(suma)]
        rectangulo[2] = puntos[np.argmax(suma)]
        
        diferencia = np.diff(puntos, axis=1)
        rectangulo[1] = puntos[np.argmin(diferencia)]
        rectangulo[3] = puntos[np.argmax(diferencia)]
        
        return rectangulo
    
    def rectificar_metodo2(self, h):
        """
        Función rectify del método 2.
        """
        h = h.reshape((4, 2))
        h_nuevo = np.zeros((4, 2), dtype=np.float32)
        
        suma = h.sum(1)
        h_nuevo[0] = h[np.argmin(suma)]
        h_nuevo[2] = h[np.argmax(suma)]
        
        diferencia = np.diff(h, axis=1)
        h_nuevo[1] = h[np.argmin(diferencia)]
        h_nuevo[3] = h[np.argmax(diferencia)]
        
        return h_nuevo
    
    def preprocesar_para_deteccion(self, imagen: np.ndarray, metodo: int = 1) -> np.ndarray:
        """
        Preprocesamiento suave solo para detección de bordes.
        """
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        if metodo == 1:
            difuminada = cv2.GaussianBlur(gris, 
                                        (self.configuracion_metodo1['kernel_gaussiano'], 
                                         self.configuracion_metodo1['kernel_gaussiano']), 0.8)
            bordes = cv2.Canny(difuminada, 
                              self.configuracion_metodo1['canny_bajo'], 
                              self.configuracion_metodo1['canny_alto'])
        else:
            difuminada = cv2.GaussianBlur(gris, 
                                        (self.configuracion_metodo2['kernel_gaussiano'], 
                                         self.configuracion_metodo2['kernel_gaussiano']), 0.8)
            bordes = cv2.Canny(difuminada, 
                              self.configuracion_metodo2['canny_bajo'], 
                              self.configuracion_metodo2['canny_alto'])
        
        return bordes
    
    def encontrar_contornos_documento_metodo1(self, bordes: np.ndarray) -> List[np.ndarray]:
        """
        Encuentra contornos usando el Método 1.
        """
        contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contornos_documento = []
        area_imagen = bordes.shape[0] * bordes.shape[1]
        
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            
            if area > area_imagen * self.ratio_area_minima:
                epsilon = self.configuracion_metodo1['factor_epsilon'] * cv2.arcLength(contorno, True)
                aproximacion = cv2.approxPolyDP(contorno, epsilon, True)
                
                if len(aproximacion) == 4:
                    contornos_documento.append(aproximacion)
        
        return contornos_documento
    
    def encontrar_contorno_documento_metodo2(self, bordes: np.ndarray) -> Optional[np.ndarray]:
        """
        Encuentra contorno usando el Método 2.
        """
        contornos, _ = cv2.findContours(bordes, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        if not contornos:
            return None
        
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
        area_imagen = bordes.shape[0] * bordes.shape[1]
        
        for c in contornos:
            area = cv2.contourArea(c)
            
            if area < area_imagen * self.ratio_area_minima:
                continue
            
            perimetro = cv2.arcLength(c, True)
            aproximacion = cv2.approxPolyDP(c, self.configuracion_metodo2['factor_epsilon'] * perimetro, True)
            
            if len(aproximacion) == 4:
                return aproximacion
        
        return None
    
    def transformacion_cuatro_puntos_alta_resolucion(self, imagen_original: np.ndarray, puntos: np.ndarray) -> np.ndarray:
        """
        Transformación de perspectiva en alta resolución usando imagen original.
        """
        rectangulo = self.ordenar_puntos_metodo1(puntos)
        (esquina_sup_izq, esquina_sup_der, esquina_inf_der, esquina_inf_izq) = rectangulo
        
        ancho_a = np.sqrt(((esquina_inf_der[0] - esquina_inf_izq[0]) ** 2) + ((esquina_inf_der[1] - esquina_inf_izq[1]) ** 2))
        ancho_b = np.sqrt(((esquina_sup_der[0] - esquina_sup_izq[0]) ** 2) + ((esquina_sup_der[1] - esquina_sup_izq[1]) ** 2))
        ancho_maximo = max(int(ancho_a), int(ancho_b))
        
        altura_a = np.sqrt(((esquina_sup_der[0] - esquina_inf_der[0]) ** 2) + ((esquina_sup_der[1] - esquina_inf_der[1]) ** 2))
        altura_b = np.sqrt(((esquina_sup_izq[0] - esquina_inf_izq[0]) ** 2) + ((esquina_sup_izq[1] - esquina_inf_izq[1]) ** 2))
        altura_maxima = max(int(altura_a), int(altura_b))
        
        destino = np.array([
            [0, 0],
            [ancho_maximo - 1, 0],
            [ancho_maximo - 1, altura_maxima - 1],
            [0, altura_maxima - 1]
        ], dtype="float32")
        
        matriz_transformacion = cv2.getPerspectiveTransform(rectangulo, destino)
        transformada = cv2.warpPerspective(imagen_original, matriz_transformacion, (ancho_maximo, altura_maxima))
        
        return transformada
    
    def detectar_metodo1_alta_resolucion(self, imagen_original: np.ndarray) -> Tuple[np.ndarray, bool]:
        """
        Método 1: Detección en imagen pequeña, transformación en imagen original.
        """
        try:
            imagen_deteccion, factor_escala = self.redimensionar_solo_para_deteccion(imagen_original)
            bordes = self.preprocesar_para_deteccion(imagen_deteccion, metodo=1)
            contornos_documento = self.encontrar_contornos_documento_metodo1(bordes)
            
            if not contornos_documento:
                return imagen_original.copy(), False
            
            contorno_mayor = max(contornos_documento, key=cv2.contourArea)
            contorno_original = self.escalar_contorno_a_original(contorno_mayor, factor_escala)
            imagen_corregida = self.transformacion_cuatro_puntos_alta_resolucion(imagen_original, contorno_original.reshape(4, 2))
            
            return imagen_corregida, True

        except Exception as error:
            logger.warning("Metodo 1 de deteccion de documento fallo: %s", error)
            return imagen_original.copy(), False

    def detectar_metodo2_alta_resolucion(self, imagen_original: np.ndarray) -> Tuple[np.ndarray, bool]:
        """
        Método 2: Detección en imagen pequeña, transformación en imagen original.
        """
        try:
            imagen_deteccion, factor_escala = self.redimensionar_solo_para_deteccion(imagen_original)
            bordes = self.preprocesar_para_deteccion(imagen_deteccion, metodo=2)
            contorno_objetivo = self.encontrar_contorno_documento_metodo2(bordes)
            
            if contorno_objetivo is None:
                return imagen_original.copy(), False
            
            contorno_original = self.escalar_contorno_a_original(contorno_objetivo, factor_escala)
            puntos_rectangulo = self.rectificar_metodo2(contorno_original)
            
            ancho1 = np.linalg.norm(puntos_rectangulo[1] - puntos_rectangulo[0])
            ancho2 = np.linalg.norm(puntos_rectangulo[2] - puntos_rectangulo[3])
            altura1 = np.linalg.norm(puntos_rectangulo[3] - puntos_rectangulo[0])
            altura2 = np.linalg.norm(puntos_rectangulo[2] - puntos_rectangulo[1])
            
            ancho_documento = int((ancho1 + ancho2) / 2)
            altura_documento = int((altura1 + altura2) / 2)
            
            puntos_destino = np.array([
                [0, 0], 
                [ancho_documento, 0], 
                [ancho_documento, altura_documento], 
                [0, altura_documento]
            ], dtype=np.float32)
            matriz_transformacion = cv2.getPerspectiveTransform(puntos_rectangulo.astype(np.float32), puntos_destino)
            corregida = cv2.warpPerspective(imagen_original, matriz_transformacion, (ancho_documento, altura_documento))
            
            return corregida, True

        except Exception as error:
            logger.warning("Metodo 2 de deteccion de documento fallo: %s", error)
            return imagen_original.copy(), False

    def detectar_y_corregir_alta_resolucion(self, imagen: np.ndarray, metodo_preferido: int = 1) -> Tuple[np.ndarray, bool]:
        """
        Sistema dual de alta resolución que mantiene calidad original.
        """
        imagen_procesada, ruido_filtrado, nivel_ruido = self.estimar_ruido_y_filtrar(imagen)
        
        metodos = [self.detectar_metodo1_alta_resolucion, self.detectar_metodo2_alta_resolucion]
        
        if metodo_preferido == 2:
            metodos.reverse()
        
        # Intentar primer método
        corregida, exito = metodos[0](imagen_procesada)
        
        if exito:
            return corregida, True
        
        # Si el primer método falla, intentar el segundo
        corregida, exito = metodos[1](imagen_procesada)
        
        return corregida, exito


class ProcesadorDocumentos:
    """
    Clase principal que maneja todo el proceso de detección y mejora de documentos.
    """
    
    def __init__(self, ratio_area_minima: float = 0.05, dimension_maxima: int = 1500, umbral_ruido: float = 12.0):
        """
        Inicializa el procesador de documentos.
        
        Args:
            ratio_area_minima: Ratio mínimo del área del documento respecto a la imagen
            dimension_maxima: Dimensión máxima para redimensionar SOLO para detección
            umbral_ruido: Umbral de ruido para aplicar filtro de suavizado
        """
        self.detector = DetectorDocumentosDual(
            ratio_area_minima=ratio_area_minima,
            dimension_maxima=dimension_maxima,
            umbral_ruido=umbral_ruido
        )
        
    def procesar_documento(self, ruta_imagen: str, ruta_salida: str = "documento_corregido.jpg", 
                          metodo_preferido: int = 1) -> bool:
        """
        Procesa un documento completo: detección, corrección y mejora.
        
        Args:
            ruta_imagen: Ruta de la imagen de entrada
            ruta_salida: Ruta donde guardar el resultado
            metodo_preferido: Método preferido (1 o 2)
            
        Returns:
            bool: True si el procesamiento fue exitoso, False en caso contrario
        """
        try:
            # Cargar imagen
            imagen = cv2.imread(ruta_imagen)
            if imagen is None:
                return False
            
            # Detectar y corregir documento
            corregida, exito = self.detector.detectar_y_corregir_alta_resolucion(imagen, metodo_preferido)
            
            if exito:
                # Aplicar mejoras de contraste y saturación
                corregida = self.detector.mejorador.procesar_imagen_completa(corregida)
            else:
                corregida = imagen.copy()
            
            # Guardar resultado
            cv2.imwrite(ruta_salida, corregida)
            
            return True

        except Exception as error:
            logger.warning("Fallo al procesar el documento %s: %s", ruta_imagen, error)
            return False

    def procesar_documento_desde_array(self, imagen: np.ndarray, ruta_salida: Optional[str] = None, 
                                     metodo_preferido: int = 1) -> Tuple[np.ndarray, bool]:
        """
        Procesa un documento desde un array numpy.
        
        Args:
            imagen: Array numpy de la imagen
            ruta_salida: Ruta donde guardar el resultado (opcional)
            metodo_preferido: Método preferido (1 o 2)
            
        Returns:
            Tuple[np.ndarray, bool]: Imagen procesada y éxito del procesamiento
        """
        try:
            # Detectar y corregir documento
            corregida, exito = self.detector.detectar_y_corregir_alta_resolucion(imagen, metodo_preferido)
            
            if exito:
                # Aplicar mejoras de contraste y saturación
                corregida = self.detector.mejorador.procesar_imagen_completa(corregida)
            else:
                corregida = imagen.copy()
            
            # Guardar si se especifica ruta
            if ruta_salida:
                cv2.imwrite(ruta_salida, corregida)
            
            return corregida, exito

        except Exception as error:
            logger.warning("Fallo al procesar la imagen en memoria: %s", error)
            return imagen.copy(), False


def main():
    """
    Función principal simplificada - solo maneja entrada y llama a la clase.
    Uso: python document_scanner.py <ruta_imagen>
    """
    if len(sys.argv) < 2:
        print("Uso: python document_scanner.py <ruta_imagen>")
        return

    ruta_imagen = sys.argv[1]

    procesador = ProcesadorDocumentos()
    exito = procesador.procesar_documento(ruta_imagen)

    if not exito:
        print("El procesamiento falló")


if __name__ == "__main__":
    main()