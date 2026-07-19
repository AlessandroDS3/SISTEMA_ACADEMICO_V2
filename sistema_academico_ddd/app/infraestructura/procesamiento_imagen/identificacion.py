import cv2
import numpy as np
from typing import Tuple, List

def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and preprocess the answer sheet image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed binary image
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not open or find the image: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Apply morphological operations to enhance marks
    kernel = np.ones((2,2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return binary

def extract_id_section(binary_image: np.ndarray) -> np.ndarray:
    """
    Extract the identification section from the answer sheet.
    
    Args:
        binary_image: Binary image of the answer sheet
        
    Returns:
        The identification section of the image
    """
    height, width = binary_image.shape
    
    # Extract the left quarter of the image (ID section)
    id_section = binary_image[:, :width//4]
    
    return id_section

def detect_filled_bubbles_in_dni(id_section: np.ndarray) -> List[int]:
    """
    Detect which bubbles are filled in the DNI section.
    
    Args:
        id_section: The identification section of the answer sheet
        
    Returns:
        List of detected DNI digits
    """
    height, width = id_section.shape

    # Define the DNI region based on the provided image
    dni_region_start_y = int(height * 0.37)
    dni_region_end_y = int(height * 0.673)
    dni_region_start_x = int(width * 0.14)
    dni_region_end_x = int(width * 0.81)

    dni_region = id_section[dni_region_start_y:dni_region_end_y, dni_region_start_x:dni_region_end_x]

    dni_height, dni_width = dni_region.shape
    num_digits = 8
    digit_cell_height = dni_height // 10
    digit_position_width = dni_width // num_digits
    start_offset = 0

    detected_dni = []

    for digit_pos in range(num_digits):
        start_x = start_offset + digit_pos * digit_position_width
        end_x = start_x + digit_position_width
        digit_column = dni_region[:, start_x:end_x]

        max_filled_value = -1
        max_filled_count = 0

        for value in range(10):
            start_y = value * digit_cell_height
            end_y = start_y + digit_cell_height

            bubble_region = digit_column[start_y:end_y, :]
            filled_count = np.sum(bubble_region) // 255

            if filled_count > max_filled_count:
                max_filled_count = filled_count
                max_filled_value = value

        detected_dni.append(max_filled_value)

    return detected_dni

def detect_application_area(id_section: np.ndarray) -> str:
    """
    Detect which area the student is applying to.
    
    Args:
        id_section: The identification section of the answer sheet
        
    Returns:
        The detected application area (Ingenierías, Biomédicas, or Sociales)
    """
    height, width = id_section.shape
    
    area_region_start_y = int(height * 0.19)
    area_region_end_y = int(height * 0.23)
    area_region_start_x = int(width * 0.645)
    area_region_end_x = int(width * 0.864)
    
    if area_region_end_y >= height:
        area_region_end_y = height - 1
    if area_region_end_x >= width:
        area_region_end_x = width - 1
    
    area_region = id_section[area_region_start_y:area_region_end_y, 
                            area_region_start_x:area_region_end_x]
    
    area_height, area_width = area_region.shape
    area_width_third = area_width // 3
    areas = [1, 2, 3]
    area_filled_counts = []
    
    max_filled_count = 0
    selected_area_index = 0
    
    for i in range(3):
        start_x = i * area_width_third
        end_x = start_x + area_width_third
        bubble_region = area_region[:, start_x:end_x]
        filled_count = np.sum(bubble_region) // 255
        area_filled_counts.append(filled_count)
        
        if filled_count > max_filled_count:
            max_filled_count = filled_count
            selected_area_index = i
    
    if sum(area_filled_counts) < 10:
        return " "
    
    return str(areas[selected_area_index])

def process_answer_sheet(image_path: str) -> Tuple[List[int], str]:
    """
    Process the answer sheet image to extract student identification information.
    
    Args:
        image_path: Path to the answer sheet image
        
    Returns:
        Tuple of (DNI digits, application area)
    """
    try:
        # Load and preprocess the image
        binary_image = load_and_preprocess_image(image_path)
        
        # Extract identification section
        id_section = extract_id_section(binary_image)
        
        # Detect DNI
        dni = detect_filled_bubbles_in_dni(id_section)
        
        # Detect application area
        area = detect_application_area(id_section)
        
        return dni, area
        
    except Exception as e:
        print(f"Error processing answer sheet: {str(e)}")
        return [], ""

if __name__ == "__main__":
    # Replace this with the path to your answer sheet image
    image_path = "documento_final.jpg"
    
    dni, area = process_answer_sheet(image_path)
    final_dni = ''.join(map(str, dni))
    
    print(f"DNI: {final_dni}")
    print(f"Area: {area}")