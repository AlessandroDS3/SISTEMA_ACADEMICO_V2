import cv2
import numpy as np
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

def cargar_y_preprocesar_imagen(ruta_imagen: str) -> np.ndarray:
    """
    Carga y preprocesa la imagen de la hoja de respuestas.

    Args:
        ruta_imagen: Ruta al archivo de imagen

    Returns:
        Imagen binaria preprocesada
    """
    img = cv2.imread(ruta_imagen)
    if img is None:
        raise FileNotFoundError(f"No se pudo abrir o encontrar la imagen: {ruta_imagen}")

    # Convertir a escala de grises
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral para obtener imagen binaria
    _, binaria = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY_INV)

    # Aplicar operaciones morfológicas para resaltar las marcas
    kernel = np.ones((2,2), np.uint8)
    binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)

    return binaria

def extraer_seccion_identificacion(imagen_binaria: np.ndarray) -> np.ndarray:
    """
    Extrae la sección de identificación de la hoja de respuestas.

    Args:
        imagen_binaria: Imagen binaria de la hoja de respuestas

    Returns:
        La sección de identificación de la imagen
    """
    alto, ancho = imagen_binaria.shape

    # Extrae el cuarto izquierdo de la imagen (sección de identificación)
    seccion_id = imagen_binaria[:, :ancho//4]

    return seccion_id

def detectar_burbujas_llenas_dni(seccion_id: np.ndarray) -> List[int]:
    """
    Detecta qué burbujas están marcadas en la sección de DNI.

    Args:
        seccion_id: La sección de identificación de la hoja de respuestas

    Returns:
        Lista de dígitos de DNI detectados
    """
    alto, ancho = seccion_id.shape

    # Región del DNI definida a partir de las proporciones de la hoja de referencia
    dni_inicio_y = int(alto * 0.37)
    dni_fin_y = int(alto * 0.673)
    dni_inicio_x = int(ancho * 0.14)
    dni_fin_x = int(ancho * 0.81)

    region_dni = seccion_id[dni_inicio_y:dni_fin_y, dni_inicio_x:dni_fin_x]

    alto_dni, ancho_dni = region_dni.shape
    num_digitos = 8
    alto_celda_digito = alto_dni // 10
    ancho_posicion_digito = ancho_dni // num_digitos

    dni_detectado = []

    for posicion_digito in range(num_digitos):
        inicio_x = posicion_digito * ancho_posicion_digito
        fin_x = inicio_x + ancho_posicion_digito
        columna_digito = region_dni[:, inicio_x:fin_x]

        valor_max_llenado = -1
        conteo_max_llenado = 0

        for valor in range(10):
            inicio_y = valor * alto_celda_digito
            fin_y = inicio_y + alto_celda_digito

            region_burbuja = columna_digito[inicio_y:fin_y, :]
            conteo_llenado = np.sum(region_burbuja) // 255

            if conteo_llenado > conteo_max_llenado:
                conteo_max_llenado = conteo_llenado
                valor_max_llenado = valor

        dni_detectado.append(valor_max_llenado)

    return dni_detectado

def detectar_area_postulacion(seccion_id: np.ndarray) -> str:
    """
    Detecta a qué área está postulando el estudiante.

    Args:
        seccion_id: La sección de identificación de la hoja de respuestas

    Returns:
        El área de postulación detectada (Ingenierías, Biomédicas o Sociales)
    """
    alto, ancho = seccion_id.shape

    area_inicio_y = int(alto * 0.19)
    area_fin_y = int(alto * 0.23)
    area_inicio_x = int(ancho * 0.645)
    area_fin_x = int(ancho * 0.864)

    if area_fin_y >= alto:
        area_fin_y = alto - 1
    if area_fin_x >= ancho:
        area_fin_x = ancho - 1

    region_area = seccion_id[area_inicio_y:area_fin_y, area_inicio_x:area_fin_x]

    _, ancho_area = region_area.shape
    tercio_ancho_area = ancho_area // 3
    areas = [1, 2, 3]
    conteos_llenado_area = []

    conteo_max_llenado = 0
    indice_area_seleccionada = 0

    for i in range(3):
        inicio_x = i * tercio_ancho_area
        fin_x = inicio_x + tercio_ancho_area
        region_burbuja = region_area[:, inicio_x:fin_x]
        conteo_llenado = np.sum(region_burbuja) // 255
        conteos_llenado_area.append(conteo_llenado)

        if conteo_llenado > conteo_max_llenado:
            conteo_max_llenado = conteo_llenado
            indice_area_seleccionada = i

    if sum(conteos_llenado_area) < 10:
        return " "

    return str(areas[indice_area_seleccionada])

def procesar_hoja_respuestas(ruta_imagen: str) -> Tuple[List[int], str]:
    """
    Procesa la imagen de la hoja de respuestas para extraer la identificación del estudiante.

    Args:
        ruta_imagen: Ruta a la imagen de la hoja de respuestas

    Returns:
        Tupla (dígitos del DNI, área de postulación)
    """
    try:
        imagen_binaria = cargar_y_preprocesar_imagen(ruta_imagen)
        seccion_id = extraer_seccion_identificacion(imagen_binaria)

        dni = detectar_burbujas_llenas_dni(seccion_id)
        area = detectar_area_postulacion(seccion_id)

        return dni, area

    except Exception as error:
        logger.warning("Error al procesar la hoja de respuestas %s: %s", ruta_imagen, error)
        return [], ""

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python identificacion.py <ruta_imagen>")
        sys.exit(1)

    dni, area = procesar_hoja_respuestas(sys.argv[1])
    dni_final = ''.join(map(str, dni))

    print(f"DNI: {dni_final}")
    print(f"Area: {area}")