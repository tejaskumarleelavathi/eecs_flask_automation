import sys
import logging
import pandas as pd
import time
import os
import json
from library.excel_data_manipulation import DataProcessor
from library.url_link_extractor import WebScraper
from library.utils import (
    save_to_csv,
    save_to_json,
    save_to_text,
    process_links
    )
from library.constants import LINK_FILE,PDF_DATA

# Configure logging
logging.basicConfig(
    filename='data_processor.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Command-line interface for running the DataProcessor
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file_path> <output_directory>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_directory = "urls_folder"


    processor = DataProcessor(input_file_path)
    scraper = WebScraper()

    if processor.read_file():
        professor_websites = processor.get_professor_websites()
        professor_link_data = []

        for professor, website in professor_websites:
            sub_links = scraper.extract_navigation_links(website)
            professor_link_data.append({
                "Professor Name": professor,
                "Main Website": website,
                "Sub Links": sub_links
            })

        # Save data in different formats
        start_time = time.time()
        save_to_csv(professor_link_data, output_directory)
        logging.info(f"Time taken to save CSV: {time.time() - start_time:.2f} seconds")

        start_time = time.time()
        save_to_json(professor_link_data, output_directory)
        logging.info(f"Time taken to save JSON: {time.time() - start_time:.2f} seconds")

        start_time = time.time()
        save_to_text(professor_link_data, output_directory)
        logging.info(f"Time taken to save Text: {time.time() - start_time:.2f} seconds")

        print(f"Data processing complete. Output saved to {output_directory}")
    else:
        print("File reading failed. Check the log for more details.")

    link_file = LINK_FILE
    pdf_data = PDF_DATA
    process_links(link_file,PDF_DATA)
if __name__ == "__main__":
    main()
