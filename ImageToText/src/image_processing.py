import pytesseract
from pdf2image import convert_from_path
from ImageToText.log.logger import get_logger
import traceback

# Set up the logger
logger = get_logger("image_processing")


def extract_text_from_pdf(input_pdf_path):
    """
    Extracts text from a PDF file, including scanned pages (images).
    
    Args:
    input_pdf_path (str): Path to the PDF file to be processed.

    Returns:
    str: Extracted text from the PDF file.
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(input_pdf_path)
        extracted_text = ""

        for image in images:
            # Use Tesseract to perform OCR on each image
            text = pytesseract.image_to_string(image)
            extracted_text += text + "\n"

        logger.info("Successfully extracted text from PDF: %s", input_pdf_path)
    except Exception as e:
        logger.error("Error occurred while extracting text from PDF: %s", str(e))
        logger.error(traceback.format_exc())
        extracted_text = ""

    return extracted_text
