import cv2
import numpy as np
from math import atan2, sqrt
from itertools import combinations
from skimage import exposure
import logging
import os
import sys

logger = logging.getLogger(__name__)

def eliminar_sombras(ruta_imagen, ruta_salida, tamano_kernel_desenfoque=25, gamma=1.5, ancho_objetivo=1000):
    """
    Elimina sombras de una imagen para mejorar la detección de esquinas
    """
    img = cv2.imread(ruta_imagen)
    if img is None:
        return None
    
    # Redimensionar imagen
    alto, ancho = img.shape[:2]
    relacion_aspecto = alto / ancho
    nuevo_alto = int(ancho_objetivo * relacion_aspecto)
    img_redimensionada = cv2.resize(img, (ancho_objetivo, nuevo_alto))
    
    # Procesamiento para eliminar sombras
    grises = cv2.cvtColor(img_redimensionada, cv2.COLOR_BGR2GRAY)
    desenfocado = cv2.GaussianBlur(grises, (tamano_kernel_desenfoque, tamano_kernel_desenfoque), 0)
    dividido = cv2.divide(grises, desenfocado, scale=255)
    ecualizado = exposure.equalize_adapthist(dividido / 255.0, clip_limit=0.03)
    ecualizado = (ecualizado * 255).astype(np.uint8)
    corregido = exposure.adjust_gamma(ecualizado, gamma=int(gamma))
    
    # Crear carpeta de salida solo si es necesario
    carpeta = os.path.dirname(ruta_salida)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    
    # Guardar imagen procesada
    cv2.imwrite(ruta_salida, corregido)
    return ruta_salida

def redimensionar_si_grande(imagen, tamano_maximo=2000):
    """Redimensiona la imagen si es muy grande y devuelve el factor de escala"""
    alto, ancho = imagen.shape[:2]
    if max(alto, ancho) > tamano_maximo:
        factor_escala = tamano_maximo / float(max(alto, ancho))
        redimensionada = cv2.resize(imagen, None, fx=factor_escala, fy=factor_escala, interpolation=cv2.INTER_AREA)
        return redimensionada, factor_escala
    return imagen, 1.0

def calcular_angulo(p1, p2, p3):
    """Calcula el ángulo entre tres puntos (p2 es el vértice)"""
    v1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    
    producto_punto = np.dot(v1, v2)
    magnitud1 = np.linalg.norm(v1)
    magnitud2 = np.linalg.norm(v2)
    
    if magnitud1 == 0 or magnitud2 == 0:
        return 0
    
    cos_angulo = producto_punto / (magnitud1 * magnitud2)
    cos_angulo = np.clip(cos_angulo, -1, 1)
    angulo_rad = np.arccos(cos_angulo)
    angulo_grados = np.degrees(angulo_rad)
    
    return angulo_grados

def calcular_area_rectangulo(puntos):
    """Calcula el área del rectángulo formado por 4 puntos"""
    if len(puntos) != 4:
        return 0
    
    cx = sum(p[0] for p in puntos) / 4
    cy = sum(p[1] for p in puntos) / 4
    
    def angulo_desde_centro(punto):
        return atan2(punto[1] - cy, punto[0] - cx)
    
    puntos_ordenados = sorted(puntos, key=angulo_desde_centro)
    
    area = 0
    n = len(puntos_ordenados)
    for i in range(n):
        j = (i + 1) % n
        area += puntos_ordenados[i][0] * puntos_ordenados[j][1]
        area -= puntos_ordenados[j][0] * puntos_ordenados[i][1]
    
    return abs(area) / 2

def distancia_entre_puntos(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos"""
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def es_rectangulo_valido(puntos, angulo_minimo=75, angulo_maximo=105, ratio_distancia_minima=0.1):
    """
    Verifica si 4 puntos forman un rectángulo válido
    """
    if len(puntos) != 4:
        return False, [], 0
    
    cx = sum(p[0] for p in puntos) / 4
    cy = sum(p[1] for p in puntos) / 4
    
    def angulo_desde_centro(punto):
        return atan2(punto[1] - cy, punto[0] - cx)
    
    puntos_ordenados = sorted(puntos, key=angulo_desde_centro)
    
    angulos = []
    for i in range(4):
        p1 = puntos_ordenados[i]
        p2 = puntos_ordenados[(i + 1) % 4]
        p3 = puntos_ordenados[(i + 2) % 4]
        angulo = calcular_angulo(p1, p2, p3)
        angulos.append(angulo)
    
    angulos_validos = all(angulo_minimo <= angulo <= angulo_maximo for angulo in angulos)
    
    distancias = []
    for i in range(4):
        for j in range(i + 1, 4):
            distancia = distancia_entre_puntos(puntos_ordenados[i], puntos_ordenados[j])
            distancias.append(distancia)
    
    distancia_maxima = max(distancias)
    distancia_minima = min(distancias)
    ratio_distancia = distancia_minima / distancia_maxima if distancia_maxima > 0 else 0
    distribucion_valida = ratio_distancia >= ratio_distancia_minima
    
    return angulos_validos and distribucion_valida, angulos, ratio_distancia

def encontrar_cuadrados_esquina_personalizado(imagen, 
                                            factor_area_minima=0.0001, factor_area_maxima=5,
                                            vertices_minimos=3, vertices_maximos=6,
                                            aspecto_minimo=0.3, aspecto_maximo=3.0,
                                            angulo_minimo=75, angulo_maximo=105,
                                            ratio_distancia_minima=0.1, factor_area_rectangulo_minima=0.1,
                                            factor_epsilon=0.02):
    """
    Detecta cuadrados de esquina con parámetros personalizables
    """
    img, escala = redimensionar_si_grande(imagen.copy())
    alto, ancho = img.shape[:2]
    
    grises = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Métodos de detección
    metodos_deteccion = []
    
    umbral_adaptativo = cv2.adaptiveThreshold(grises, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY_INV, 11, 2)
    metodos_deteccion.append(umbral_adaptativo)
    
    ecualizado = cv2.equalizeHist(grises)
    _, umbral_fijo = cv2.threshold(ecualizado, 127, 255, cv2.THRESH_BINARY_INV)
    metodos_deteccion.append(umbral_fijo)
    
    for valor_umbral in [80, 100, 120, 130, 140, 160, 180, 190, 210]:
        _, umbral = cv2.threshold(grises, valor_umbral, 255, cv2.THRESH_BINARY_INV)
        metodos_deteccion.append(umbral)
    
    desenfocado = cv2.GaussianBlur(grises, (5, 5), 0)
    _, umbral_desenfocado = cv2.threshold(desenfocado, 140, 255, cv2.THRESH_BINARY_INV)
    metodos_deteccion.append(umbral_desenfocado)
    
    mejores_cuadrados = []
    mejor_puntuacion = 0
    
    for imagen_binaria in metodos_deteccion:
        contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        area_minima = (ancho * alto) * factor_area_minima
        area_maxima = (ancho * alto) * factor_area_maxima
        
        candidatos_cuadrados = []
        
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            
            if area_minima < area < area_maxima:
                epsilon = factor_epsilon * cv2.arcLength(contorno, True)
                aproximacion = cv2.approxPolyDP(contorno, epsilon, True)
                
                if vertices_minimos <= len(aproximacion) <= vertices_maximos:
                    x, y, ancho_contorno, alto_contorno = cv2.boundingRect(aproximacion)
                    relacion_aspecto = float(ancho_contorno) / alto_contorno
                    
                    if aspecto_minimo <= relacion_aspecto <= aspecto_maximo:
                        M = cv2.moments(contorno)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            candidatos_cuadrados.append({
                                'centro': (cx, cy),
                                'contorno': contorno,
                                'area': area,
                                'relacion_aspecto': relacion_aspecto
                            })
        
        mejor_combinacion_este_metodo = None
        mejor_puntuacion_rectangulo_este_metodo = 0
        
        if len(candidatos_cuadrados) >= 4:
            contador_combinaciones = 0
            max_combinaciones_probar = 500
            
            for combo in combinations(candidatos_cuadrados, 4):
                contador_combinaciones += 1
                if contador_combinaciones > max_combinaciones_probar:
                    break
                    
                centros = [c['centro'] for c in combo]
                es_valido, angulos, ratio_distancia = es_rectangulo_valido(centros, angulo_minimo, angulo_maximo, ratio_distancia_minima)
                
                if es_valido:
                    area_rectangulo = calcular_area_rectangulo(centros)
                    area_minima_requerida = factor_area_rectangulo_minima * (ancho * alto)
                    if area_rectangulo < area_minima_requerida:
                        continue 
                    
                    puntuacion_angulo = 1.0 - (sum(abs(90 - angulo) for angulo in angulos) / (4 * 90))
                    area_maxima_posible = ancho * alto
                    puntuacion_area = area_rectangulo / area_maxima_posible
                    puntuacion_total = (puntuacion_area * 0.5) + (puntuacion_angulo * 0.35) + (ratio_distancia * 0.15)
                    
                    if puntuacion_total > mejor_puntuacion_rectangulo_este_metodo:
                        mejor_puntuacion_rectangulo_este_metodo = puntuacion_total
                        mejor_combinacion_este_metodo = combo
            
            if mejor_combinacion_este_metodo and mejor_puntuacion_rectangulo_este_metodo > mejor_puntuacion:
                mejor_puntuacion = mejor_puntuacion_rectangulo_este_metodo
                mejores_cuadrados = mejor_combinacion_este_metodo
    
    if mejores_cuadrados:
        info_esquinas = []
        for i, cuadrado in enumerate(mejores_cuadrados):
            centro = cuadrado['centro']
            area = cuadrado['area']
            info_esquinas.append({
                'id': i + 1,
                'centro': centro,
                'area': area,
                'contorno': cuadrado['contorno']
            })
        
        centros = [c['centro'] for c in info_esquinas]
        centro_hoja_x = sum(c[0] for c in centros) / 4
        centro_hoja_y = sum(c[1] for c in centros) / 4
        
        def clasificar_esquina(centro, hoja_cx, hoja_cy):
            x, y = centro
            if x < hoja_cx and y < hoja_cy:
                return 'superior-izquierda'
            elif x >= hoja_cx and y < hoja_cy:
                return 'superior-derecha'
            elif x >= hoja_cx and y >= hoja_cy:
                return 'inferior-derecha'
            else:
                return 'inferior-izquierda'
        
        for esquina in info_esquinas:
            esquina['posicion'] = clasificar_esquina(esquina['centro'], centro_hoja_x, centro_hoja_y)
        
        return info_esquinas
    
    return None

def encontrar_cuadrados_esquina(imagen):
    """Función con parámetros por defecto"""
    return encontrar_cuadrados_esquina_personalizado(imagen)

def corregir_perspectiva(img, cuadrados_esquina):
    """Corrige la perspectiva de la imagen basándose en los cuadrados de esquina"""
    posiciones_esquinas = {esquina['posicion']: esquina['centro'] for esquina in cuadrados_esquina}
    
    puntos_origen = np.array([
        posiciones_esquinas['superior-izquierda'],
        posiciones_esquinas['superior-derecha'], 
        posiciones_esquinas['inferior-derecha'],
        posiciones_esquinas['inferior-izquierda']
    ], dtype=np.float32)
    
    ancho_superior = np.linalg.norm(puntos_origen[0] - puntos_origen[1])
    ancho_inferior = np.linalg.norm(puntos_origen[3] - puntos_origen[2])
    ancho = max(int(ancho_superior), int(ancho_inferior))

    alto_izquierda = np.linalg.norm(puntos_origen[0] - puntos_origen[3])
    alto_derecha = np.linalg.norm(puntos_origen[1] - puntos_origen[2])
    alto = max(int(alto_izquierda), int(alto_derecha))

    puntos_destino = np.array([
        [0, 0],
        [ancho - 1, 0],
        [ancho - 1, alto - 1],
        [0, alto - 1]
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
    corregida = cv2.warpPerspective(img, M, (ancho, alto))

    return corregida

def procesar_hoja_examen(ruta_imagen, guardar_resultado=True, ruta_salida="hoja_corregida.jpg"):
    """
    Procesa una hoja de examen detectando cuadrados de esquina y corrigiendo perspectiva
    """
    img_original = cv2.imread(ruta_imagen)
    if img_original is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")
    
    img_redimensionada, escala = redimensionar_si_grande(img_original)
    
    # Detectar cuadrados sobre imagen redimensionada
    cuadrados_esquina = encontrar_cuadrados_esquina(img_redimensionada)
    
    if cuadrados_esquina:
        # Ajustar coordenadas de los cuadrados a la imagen original
        for esquina in cuadrados_esquina:
            x, y = esquina['centro']
            esquina['centro'] = (int(x / escala), int(y / escala))
            esquina['contorno'] = (esquina['contorno'] / escala).astype(np.int32)

        # Corregir perspectiva sobre la imagen original
        img_corregida = corregir_perspectiva(img_original, cuadrados_esquina)
        
        if guardar_resultado:
            cv2.imwrite(ruta_salida, img_corregida)
        
        return cuadrados_esquina, img_corregida
    else:
        return None, None

def detectar_con_respaldo(ruta_imagen, guardar_resultado=True):
    """
    Intenta detectar cuadrados aplicando eliminación de sombras después de cada intento fallido
    """
    img_original = cv2.imread(ruta_imagen)
    if img_original is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")
    
    # Configuraciones a probar en orden
    configuraciones = [
        {
            'nombre': 'Por defecto',
            'parametros': {}
        },
        {
            'nombre': 'Cuadrados MUY PEQUEÑOS',
            'parametros': {
                'factor_area_minima': 0.000001,
                'factor_area_maxima': 0.02,
                'vertices_minimos': 3,
                'vertices_maximos': 8,
                'aspecto_minimo': 0.2,
                'aspecto_maximo': 5.0,
                'angulo_minimo': 60,
                'angulo_maximo': 120,
                'ratio_distancia_minima': 0.05,
                'factor_area_rectangulo_minima': 0.05,
                'factor_epsilon': 0.01
            }
        },
        {
            'nombre': 'Cuadrados GRANDES',
            'parametros': {
                'factor_area_minima': 0.001,
                'factor_area_maxima': 0.2,
                'vertices_minimos': 4,
                'vertices_maximos': 4,
                'aspecto_minimo': 0.5,
                'aspecto_maximo': 2.0,
                'angulo_minimo': 80,
                'angulo_maximo': 100,
                'factor_epsilon': 0.05
            }
        },
        {
            'nombre': 'SÚPER FLEXIBLE',
            'parametros': {
                'factor_area_minima': 0.0000005,
                'factor_area_maxima': 0.3,
                'vertices_minimos': 3,
                'vertices_maximos': 10,
                'aspecto_minimo': 0.1,
                'aspecto_maximo': 10.0,
                'angulo_minimo': 50,
                'angulo_maximo': 130,
                'ratio_distancia_minima': 0.01,
                'factor_area_rectangulo_minima': 0.01,
                'factor_epsilon': 0.1
            }
        }
    ]
    
    ruta_temporal_sombra = "temp_sombra_eliminada.jpg"
    
    def intentar_deteccion(img_para_deteccion, nombre_configuracion, parametros_configuracion, es_sombra_eliminada=False):
        """
        Intenta detectar con una configuración específica
        """
        img_redimensionada, escala = redimensionar_si_grande(img_para_deteccion)
        
        esquinas = encontrar_cuadrados_esquina_personalizado(img_redimensionada, **parametros_configuracion)
        
        if esquinas:
            # Ajustar coordenadas según la escala de la imagen de detección
            for esquina in esquinas:
                x, y = esquina['centro']
                esquina['centro'] = (int(x / escala), int(y / escala))
                esquina['contorno'] = (esquina['contorno'] / escala).astype(np.int32)
            
            # Si se detectó en imagen sin sombras, convertir coordenadas
            if es_sombra_eliminada:
                esquinas_para_original = convertir_coordenadas_a_original(esquinas, img_para_deteccion, img_original)
            else:
                esquinas_para_original = esquinas
            
            # Aplicar corrección de perspectiva a la imagen original
            img_corregida = corregir_perspectiva(img_original, esquinas_para_original)
            
            if guardar_resultado:
                cv2.imwrite("hoja_corregida.jpg", img_corregida)
            
            return esquinas_para_original, img_corregida
        
        return None, None
    
    def convertir_coordenadas_a_original(esquinas_sombra, img_sombra, img_original):
        """
        Convierte coordenadas detectadas en imagen sin sombras a coordenadas de imagen original
        """
        alto_sombra, ancho_sombra = img_sombra.shape[:2]
        alto_original, ancho_original = img_original.shape[:2]
        
        escala_x = ancho_original / ancho_sombra
        escala_y = alto_original / alto_sombra
        
        esquinas_original = []
        for esquina in esquinas_sombra:
            x, y = esquina['centro']
            nuevo_x = int(x * escala_x)
            nuevo_y = int(y * escala_y)
            
            nueva_esquina = esquina.copy()
            nueva_esquina['centro'] = (nuevo_x, nuevo_y)
            
            if 'contorno' in esquina:
                nuevo_contorno = esquina['contorno'].copy().astype(np.float32)
                nuevo_contorno[:, :, 0] *= escala_x
                nuevo_contorno[:, :, 1] *= escala_y
                nueva_esquina['contorno'] = nuevo_contorno.astype(np.int32)
            
            esquinas_original.append(nueva_esquina)
        
        return esquinas_original
    
    def limpiar_archivo_temporal():
        """Limpia el archivo temporal"""
        try:
            if os.path.exists(ruta_temporal_sombra):
                os.remove(ruta_temporal_sombra)
        except OSError as error:
            logger.warning("No se pudo eliminar el archivo temporal %s: %s", ruta_temporal_sombra, error)
    
    # Probar cada configuración: primero imagen original, luego sin sombras
    for configuracion in configuraciones:
        # Intentar con imagen original
        esquinas, img_corregida = intentar_deteccion(img_original, configuracion['nombre'], configuracion['parametros'], False)
        
        if esquinas:
            limpiar_archivo_temporal()
            return esquinas, img_corregida
        
        # Si falla, aplicar eliminación de sombras
        resultado_sombra = eliminar_sombras(ruta_imagen, ruta_temporal_sombra)
        
        if resultado_sombra:
            img_sin_sombra = cv2.imread(ruta_temporal_sombra)
            if img_sin_sombra is not None:
                esquinas, img_corregida = intentar_deteccion(img_sin_sombra, configuracion['nombre'], configuracion['parametros'], True)
                
                if esquinas:
                    limpiar_archivo_temporal()
                    return esquinas, img_corregida
    
    limpiar_archivo_temporal()
    return None, None

# Ejemplo de uso: python corner_detector.py <ruta_imagen>
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python corner_detector.py <ruta_imagen>")
        sys.exit(1)

    esquinas, imagen_corregida = detectar_con_respaldo(sys.argv[1])

    if esquinas:
        print(f"Detectados {len(esquinas)} cuadrados de esquina")
        for esquina in esquinas:
            print(f"{esquina['posicion']}: {esquina['centro']}")
    else:
        print("No se pudieron detectar los cuadrados")