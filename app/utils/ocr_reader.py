import pytesseract
from PIL import Image
import os

# Set the path to tesseract executable if needed (uncomment and set path if not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(file_path):
    """
    Extract text from an image file using OCR.

    Args:
        file_path (str): Path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    text = ""
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error extracting text from image: {e}")
    return text
