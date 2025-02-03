from flask import Flask, render_template, jsonify
from ImageToText.src.utils import extract_and_write_pdf
from ImageToText.log.logger import get_logger
import traceback
import os

import logging
from subprocess import Popen, PIPE

# Set environment variables programmatically
os.environ['FLASK_ENV'] = 'development'
os.environ['FLASK_DEBUG'] = '1'
logger = get_logger("main")

logging.basicConfig(
    filename='data_processor.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

def extractText():
    """
    Process all PDF files in the input directory and write the extracted text into corresponding folders.

    Args:
        input_directory (str): The path to the input directory containing folders with PDFs.
        output_directory (str): The path to the output directory to store processed PDFs.

    Returns:
        str: Success or error message.
    """
    input_directory="ExtractingPDF/pdf_files"
    output_directory="ImageToText/data/Final"
    try:
        # Iterate over all folders in the input directory
        for folder_name in os.listdir(input_directory):
            folder_path = os.path.join(input_directory, folder_name)

            # Skip if it's not a directory
            if not os.path.isdir(folder_path):
                continue

            # Create corresponding folder in the output directory
            output_folder_path = os.path.join(output_directory, folder_name)
            os.makedirs(output_folder_path, exist_ok=True)

            # Iterate over all PDF files in the folder
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".pdf"):  # Process only PDF files
                    input_pdf_path = os.path.join(folder_path, file_name)
                    output_pdf_path = os.path.join(output_folder_path, file_name)

                    # Extract and write text to a new PDF
                    try:
                        extract_and_write_pdf(input_pdf_path, output_pdf_path)
                        logger.info(f"Processed {input_pdf_path} successfully.")
                    except Exception as e:
                        logger.error(f"Failed to process {input_pdf_path}: {str(e)}")
                        logger.error(traceback.format_exc())

        return "All PDFs processed successfully."
    except Exception as e:
        logger.error("An error occurred during batch processing: %s", str(e))
        logger.error(traceback.format_exc())
        return "An error occurred during batch processing."
def run_node_command():
    """
    Function to run the Node.js script 'convert.js'.
    """
    try:
        # Run the Node.js script using the `node` command
        process = Popen(['node', 'ExtractingPDF/convert.js'], stdout=PIPE, stderr=PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return f"Node Command Success: {stdout}"
        else:
            return f"Node Command Failed: {stderr}"
    except Exception as e:
        return f"An error occurred while running the Node command: {str(e)}"
@app.route('/')
def runButton():
    return render_template('button.html')


@app.route('/run-extract', methods=['POST'])
def run_extract():
    """
    Endpoint to trigger the main() function when the button is clicked.
    """
    result_pdf = run_node_command()
    result_text = extractText()
    combined_result = f"ExtractPDF: {result_pdf} | ExtractText : {result_text}"
    return jsonify({'message': combined_result})


if __name__ == '__main__':
    app.run(debug=True)
