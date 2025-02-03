# from src.image_processing import extract_text_from_pdf
# from src.utils import extract_and_write_pdf
# from log.logger import get_logger
# import traceback
#
# # Set up the logger
# logger = get_logger("main")
#
#
# def main():
#     """
#     Main function to orchestrate the process of text extraction and writing to a new PDF.
#     """
#
#     # Paths to input and output PDFs
#     input_pdf_path = "data/member.pdf"  # Replace with your input PDF file path
#     output_pdf_path = "data/output2.pdf"  # Replace with your desired output PDF file path
#
#     try:
#         # Extract and write text to a new PDF
#         extract_and_write_pdf(input_pdf_path, output_pdf_path)
#
#     except Exception as e:
#         logger.error("An error occurred during the main process: %s", str(e))
#         # Log the full traceback for debugging
#         logger.error(traceback.format_exc())
#
#
# if __name__ == "__main__":
#     # Run the main function
#     main()
