import PyPDF2
import os

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text
