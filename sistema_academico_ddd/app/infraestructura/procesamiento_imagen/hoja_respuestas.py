import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional

class ProcesadorExamenOMR:

    def __init__(self, imagen_path: str):
        self.imagen_path = imagen_path
        self.borde_ancho = 38
        self.borde_alto = 30
        self.radio_evaluacion = 13
        self.umbral_marcado = 0.7
        self.radio_busqueda = 22
        self.radio_burbuja_min = 11
        self.radio_burbuja_max = 16

        self.gray_crop = None
        self.thresh = None
        self.marcas_derechas = []
        self.marcas_inferiores = []
        self.marcas_opciones_inferiores = []
        self.grilla_respuestas = []
        self.respuestas_finales = []
        self.marked_bubbles = []

    def preprocess_image(self, gray_img):
        blurred = cv2.GaussianBlur(gray_img, (3, 3), 0)
        _, thresh_otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return thresh_otsu


    def intensificar_zonas_oscuras(self, imagen):
        """
        Intensifica las zonas oscuras de la imagen para mejorar la detección de marcas.
        Aplica múltiples técnicas de mejora de contraste.
        """
        if imagen is None:
            return None
        
        # 1. Aplicar función gamma para intensificar zonas oscuras
        gamma_corrected = np.power(imagen / 255.0, 0.7) * 255.0
        gamma_corrected = gamma_corrected.astype(np.uint8)
        
        # 2. Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_corrected = clahe.apply(gamma_corrected)
        
        # 3. Aplicar filtro de mediana para reducir ruido
        median_filtered = cv2.medianBlur(clahe_corrected, 3)
        
        # 4. Aplicar función sigmoidal para intensificar contrastes
        img_float = median_filtered.astype(np.float32) / 255.0
        
        # Aplicar función sigmoidal
        sigmoid_corrected = 1 / (1 + np.exp(-10 * (img_float - 0.5)))
        
        # Convertir de vuelta a uint8
        return (sigmoid_corrected * 255.0).astype(np.uint8)


    def detectar_burbuja_real(self, centro_teorico_x: int, centro_teorico_y: int) -> Dict:
        """Detecta la burbuja real más cercana al centro teórico"""
        if self.gray_crop is None:
            return {
                'centro_x': centro_teorico_x,
                'centro_y': centro_teorico_y,
                'radio': self.radio_evaluacion
            }
        
        # Definir región de interés (ROI)
        roi_x1 = max(0, centro_teorico_x - self.radio_busqueda)
        roi_y1 = max(0, centro_teorico_y - self.radio_busqueda)
        roi_x2 = min(self.gray_crop.shape[1], centro_teorico_x + self.radio_busqueda)
        roi_y2 = min(self.gray_crop.shape[0], centro_teorico_y + self.radio_busqueda)
        
        # Extraer ROI
        roi_gray = self.gray_crop[roi_y1:roi_y2, roi_x1:roi_x2]
        
        # Aplicar filtro Gaussiano
        roi_blurred = cv2.GaussianBlur(roi_gray, (1, 1), 0)
        
        # Detección de bordes con Canny
        roi_thresh = cv2.Canny(roi_blurred, 50, 150)
        
        # Detectar contornos
        contours, _ = cv2.findContours(roi_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Analizar cada contorno
        mejor_burbuja = None
        mejor_puntuacion = 0
        
        for contorno in contours:
            area = cv2.contourArea(contorno)
            if area < 10:
                continue
                
            perimetro = cv2.arcLength(contorno, True)
            if perimetro <= 0:
                continue
                
            # Calcular circularidad
            circularidad = 4 * np.pi * area / (perimetro * perimetro)
            
            # Encontrar círculo mínimo que encierra el contorno
            (x, y), radio = cv2.minEnclosingCircle(contorno)
            centro_x = int(x + roi_x1)
            centro_y = int(y + roi_y1)
            
            # Calcular distancia al centro teórico
            distancia = np.sqrt((centro_x - centro_teorico_x)**2 + (centro_y - centro_teorico_y)**2)
            
            # Evaluar si es una burbuja válida
            if (self.radio_burbuja_min <= radio <= self.radio_burbuja_max and
                circularidad > 0.5 and
                distancia <= self.radio_busqueda and
                area > 50):
                
                # Calcular puntuación
                puntuacion_circularidad = min(circularidad, 1.0)
                puntuacion_proximidad = 1.0 - (distancia / self.radio_busqueda)
                puntuacion_total = puntuacion_circularidad * 0.6 + puntuacion_proximidad * 0.4
                
                # Verificar si es el mejor candidato
                if puntuacion_total > mejor_puntuacion:
                    mejor_puntuacion = puntuacion_total
                    mejor_burbuja = {
                        'centro_x': centro_x,
                        'centro_y': centro_y,
                        'radio': radio
                    }
        # Si no se encontró burbuja válida, usar valores teóricos
        return mejor_burbuja or {
            'centro_x': centro_teorico_x,
            'centro_y': centro_teorico_y,
            'radio': self.radio_evaluacion
        }


    def cargar_imagen(self) -> bool:
        image = cv2.imread(self.imagen_path)
        if image is None:
            return False
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        height, width = gray.shape
        self.gray_crop = gray[0:height, width//2:]
        
        # Intensificar zonas oscuras en la mitad cortada
        self.gray_crop = self.intensificar_zonas_oscuras(self.gray_crop)
        
        thresh_adaptive = self.preprocess_image(gray)
        if thresh_adaptive is None:
            return False
        
        self.thresh = thresh_adaptive[0:height, width//2:]
        
        return True

    def extraer_franjas_guia(self):
        if self.thresh is None:
            return None, None
        franja_derecha = self.thresh[:, -self.borde_ancho:]
        franja_inferior = self.thresh[-self.borde_alto:, :]
        return franja_derecha, franja_inferior

    def detectar_marcas_guia(self):
        franja_derecha, franja_inferior = self.extraer_franjas_guia()
        
        if self.gray_crop is None:
            return
        if franja_derecha is None or franja_inferior is None:
            return
        
        height, width = self.gray_crop.shape
        
        # Detectar marcas en franja derecha
        contours_der, _ = cv2.findContours(franja_derecha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.marcas_derechas = []
        
        for cnt in contours_der:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if 4 < w < 20 and 4 < h < 20 and 30 < area < 400:
                x_global = x + (width + (width - self.borde_ancho))
                y_global = y
                if 10 < y_global < height - 10:
                    self.marcas_derechas.append((x_global, y_global, w, h))
        
        self.marcas_derechas.sort(key=lambda box: box[1])
        self.marcas_derechas = self.marcas_derechas[:30]
        
        # Detectar marcas en franja inferior
        contours_inf, _ = cv2.findContours(franja_inferior, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.marcas_inferiores = []
        
        for cnt in contours_inf:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            if 5 < w < 20 and 5 < h < 20 and 30 < area < 400:
                y_global = y + (height - self.borde_alto)
                if y_global < 1190:
                    self.marcas_inferiores.append((x, y_global, w, h))
        
        self.marcas_inferiores.sort(key=lambda box: box[0])

    def filtrar_marcas_opciones(self):
        self.marcas_opciones_inferiores = []
        
        for i in range(len(self.marcas_inferiores)):
            if (i - 2) % 7 < 5 and i >= 2:
                self.marcas_opciones_inferiores.append(self.marcas_inferiores[i])

    def detect_marked_bubbles(self, darkness_threshold=None):
        """Detección de burbujas marcadas"""
        if darkness_threshold is None:
            darkness_threshold = self.umbral_marcado
        
        if self.gray_crop is None:
            return
        
        centros_teoricos_x = [x + w // 2 for (x, y, w, h) in self.marcas_opciones_inferiores]
        centros_teoricos_y = [y + h // 2 for (x, y, w, h) in self.marcas_derechas]
        
        self.grilla_respuestas = []
        self.marked_bubbles = []
        
        # Procesar cada burbuja
        for fila_idx, centro_teorico_y in enumerate(centros_teoricos_y):
            fila = []
            
            for col_idx, centro_teorico_x in enumerate(centros_teoricos_x):
                # Usar la función para detectar burbuja real
                burbuja_real = self.detectar_burbuja_real(centro_teorico_x, centro_teorico_y)
                
                centro_real_x = burbuja_real['centro_x']
                centro_real_y = burbuja_real['centro_y']
                radio_real = burbuja_real['radio']
                
                # Crear máscara circular para medir intensidad
                mask = np.zeros(self.gray_crop.shape, dtype=np.uint8)
                cv2.circle(mask, (int(centro_real_x), int(centro_real_y)), 
                          max(1, int(radio_real - 2)), (255,), -1)
                
                mean_intensity = cv2.mean(self.gray_crop, mask=mask)[0]
                darkness = 1 - (mean_intensity / 255.0)
                marcada = darkness > darkness_threshold
                
                if marcada:
                    self.marked_bubbles.append({
                        'row': fila_idx,
                        'col': col_idx,
                        'darkness': darkness
                    })
                
                fila.append(marcada)
            
            self.grilla_respuestas.append(fila)

    def procesar_respuestas(self):
        self.respuestas_finales = []
        
        for fila_idx, fila in enumerate(self.grilla_respuestas):
            for bloque in range(3):
                inicio = bloque * 5
                fin = inicio + 5
                opciones = fila[inicio:fin]
                indices_marcados = [i for i, marcada in enumerate(opciones) if marcada]
                
                numero_pregunta = fila_idx + 1 + bloque * 30
                
                if len(indices_marcados) == 0:
                    respuesta = None
                    clasificacion = "SIN_RESPUESTA"
                elif len(indices_marcados) == 1:
                    respuesta = chr(ord('A') + indices_marcados[0])
                    clasificacion = "VALIDA"
                else:
                    respuesta = ''.join([chr(ord('A') + i) for i in indices_marcados])
                    clasificacion = "DOBLE_MARCA"
                
                self.respuestas_finales.append((numero_pregunta, respuesta, clasificacion))
        
        self.respuestas_finales.sort(key=lambda x: x[0])

    def procesar_completo(self, darkness_threshold=None) -> bool:
        """Procesamiento completo del examen OMR"""
        if not self.cargar_imagen():
            return False
        
        self.detectar_marcas_guia()
        self.filtrar_marcas_opciones()
        self.detect_marked_bubbles(darkness_threshold)
        self.procesar_respuestas()
        
        return True

    def obtener_respuestas_detectadas(self) -> List[Tuple[int, Optional[str], str]]:
        """Obtiene las respuestas detectadas"""
        return self.respuestas_finales


def main():
    """Función principal"""
    print("=== PROCESADOR OMR ===")
    imagen_path = "documento_final.jpg"
    procesador = ProcesadorExamenOMR(imagen_path)
    
    if procesador.procesar_completo():
        respuestas = procesador.obtener_respuestas_detectadas()
        
        print("Procesamiento exitoso!")
        print(f"Total respuestas: {len(respuestas)}")
        print(f"Burbujas marcadas: {len(procesador.marked_bubbles)}")
        
        # Mostrar primeras 10 respuestas
        print("\nPrimeras 10 respuestas:")
        for pregunta, respuesta, clasificacion in respuestas[:90]:
            print(f"Pregunta {pregunta}: {respuesta} ({clasificacion})")
    else:
        print("Error al procesar la imagen")

if __name__ == "__main__":
    main()