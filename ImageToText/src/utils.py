from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from ImageToText.src.image_processing import extract_text_from_pdf
from ImageToText.log.logger import get_logger
import traceback

# Set up the logger
logger = get_logger("utils")


def write_text_to_pdf(output_pdf_path, text):
    """
    Writes text content to a new PDF file with proper margins and line wrapping.
    
    Args:
    output_pdf_path (str): Path to save the output PDF file.
    text (str): Text content to write into the PDF.
    """
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        # Page size and margins
        page_width, page_height = letter
        margin_x = 50
        margin_y = 750
        right_margin = 50
        max_width = page_width - margin_x - right_margin
        line_height = 14
        current_y = margin_y

        # Set text properties
        c.setFont("Helvetica", 12)

        def wrap_line(line, max_width):
            words = line.split()
            wrapped_lines = []
            current_line = ""
            for word in words:
                test_line = f"{current_line} {word}".strip()
                if stringWidth(test_line, "Helvetica", 12) <= max_width:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)
            return wrapped_lines

        lines = text.splitlines()
        for line in lines:
            wrapped_lines = wrap_line(line, max_width)
            for wrapped_line in wrapped_lines:
                if current_y <= 50:  # Move to the next page if there's no space left
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    current_y = margin_y
                c.drawString(margin_x, current_y, wrapped_line)
                current_y -= line_height

        c.save()
        buffer.seek(0)

        with open(output_pdf_path, "wb") as f:
            f.write(buffer.getvalue())

        logger.info("Successfully wrote text to PDF: %s", output_pdf_path)
    except Exception as e:
        logger.error("Error occurred while writing text to PDF: %s", str(e))
        logger.error(traceback.format_exc())


def extract_and_write_pdf(input_pdf_path, output_pdf_path):
    """
    Extracts text from the input PDF file and writes it to a new PDF file.
    
    Args:
    input_pdf_path (str): Path to the input PDF file.
    output_pdf_path (str): Path to save the output PDF file.
    """
    try:
        extracted_text = extract_text_from_pdf(input_pdf_path)
        if extracted_text:
            write_text_to_pdf(output_pdf_path, extracted_text)
            logger.info("Text content extracted and saved to '%s' successfully.", output_pdf_path)
        else:
            logger.warning("No text was extracted from the PDF: %s", input_pdf_path)
    except Exception as e:
        logger.error("Error occurred in extract_and_write_pdf: %s", str(e))
        logger.error(traceback.format_exc())
