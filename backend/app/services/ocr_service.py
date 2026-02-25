import pytesseract
from PIL import Image
import os
from pathlib import Path

# Set Tesseract path - update this if installed in a different location
TESSERACT_PATH = r'C:\Program Files\Tessract_OCR\tesseract.exe'

def _configure_tesseract():
    """
    Configure Tesseract path.
    """
    # Check environment variable first
    env_path = os.getenv('TESSERACT_PATH')
    if env_path and os.path.exists(env_path):
        pytesseract.pytesseract.tesseract_cmd = env_path
        return
    
    # Use the hardcoded path
    if os.path.exists(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        return
    
    # Try alternative paths
    alternative_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    for path in alternative_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return
    
    # If still not found, raise error
    raise FileNotFoundError(
        f"Tesseract not found at {TESSERACT_PATH}. "
        f"Please install Tesseract or set TESSERACT_PATH environment variable."
    )

# Configure on import
try:
    _configure_tesseract()
except FileNotFoundError as e:
    print(f"Warning: {e}")

def _preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image to improve OCR accuracy.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed PIL Image
    """
    import numpy as np
    from PIL import ImageEnhance, ImageOps, ImageFilter
    import cv2
    
    # Convert to RGB if RGBA
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Resize if too small (improves OCR)
    if image.width < 800:
        ratio = 800 / image.width
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert to grayscale
    image = ImageOps.grayscale(image)
    
    # Apply Gaussian blur to reduce noise
    image = image.filter(ImageFilter.GaussianBlur(radius=1.0))
    
    # Enhance contrast significantly
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.5)
    
    # Convert to numpy array for morphological operations
    img_array = np.array(image)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_array = clahe.apply(img_array)
    
    # Apply morphological operations to clean up
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img_array = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel)
    
    # Convert back to PIL Image
    image = Image.fromarray(img_array)
    
    return image

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR with preprocessing.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted text from the image
        
    Raises:
        FileNotFoundError: If the image file doesn't exist
        Exception: If Tesseract is not installed or cannot process the image
    """
    # Validate image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Open and preprocess image
        image = Image.open(image_path)
        image = _preprocess_image(image)
        
        # Extract text with Tesseract configuration
        config = '--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=config)
        
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        raise Exception(
            "Tesseract OCR is not installed. Please install it from: "
            "https://github.com/UB-Mannheim/tesseract/wiki or set TESSERACT_PATH environment variable"
        )
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")