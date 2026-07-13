import cv2
import numpy as np

def corregir_orientacion_por_bordes(img, borde_ancho_px=100, umbral=90):
    h, w = img.shape[:2]
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    _, binary = cv2.threshold(gray, umbral, 255, cv2.THRESH_BINARY_INV)
    
    top = binary[:borde_ancho_px, :]
    bottom = binary[-borde_ancho_px:, :]
    left = binary[:, :borde_ancho_px]
    right = binary[:, -borde_ancho_px:]
    
    density_top = np.sum(top == 255) / top.size
    density_bottom = np.sum(bottom == 255) / bottom.size
    density_left = np.sum(left == 255) / left.size
    density_right = np.sum(right == 255) / right.size
    
    densities = {
        "top": density_top,
        "bottom": density_bottom,
        "left": density_left,
        "right": density_right
    }


    max_border = max(densities, key=lambda k: densities[k])

    if max_border == "top":
        rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif max_border == "bottom":
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif max_border == "left":
        rotated = cv2.rotate(img, cv2.ROTATE_180)
    else:
        rotated = img

    # Redimensionamiento A5 después de la corrección de orientación
    height_est, width_est = rotated.shape[:2]
    
    if height_est > width_est:  # Modo vertical (A5 retrato)
        dst_w, dst_h = 1169, 1654
    else:  # Modo horizontal (A5 paisaje)
        dst_w, dst_h = 1654, 1169
    
    # Redimensionar la imagen
    resized = cv2.resize(rotated, (dst_w, dst_h), interpolation=cv2.INTER_LANCZOS4)
    
    return resized

# -------------------------
# 🧪 Uso directo
# -------------------------

if __name__ == "__main__":
    ruta_entrada = "documento_final.jpg"        # Imagen recortada previamente
    ruta_salida = "imagen_orientada.jpg"         # Imagen corregida y redimensionada

    img = cv2.imread(ruta_entrada)
    if img is None:
        raise ValueError("No se pudo cargar la imagen.")

    orientada = corregir_orientacion_por_bordes(img)
    cv2.imwrite(ruta_salida, orientada)
    print(f"✅ Imagen guardada como: {ruta_salida}")