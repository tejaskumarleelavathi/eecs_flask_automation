import os
import time
import pandas as pd
import json
import requests
import pdfkit
import re
from ExtractingPDF.library.constants import WKHTHMLTOPDF
def ensure_directory_exists(directory):
    """Ensure the directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_to_csv(data, output_directory):
    """Save data to a CSV file."""
    ensure_directory_exists(output_directory)
    csv_path = os.path.join(output_directory, "professor_data.csv")
    start_time = time.time()
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"CSV file saved to {csv_path}. Time taken: {time.time() - start_time:.2f} seconds.")

def save_to_json(data, output_directory):
    """Save data to a JSON file."""
    ensure_directory_exists(output_directory)
    json_path = os.path.join(output_directory, "professor_data.json")
    start_time = time.time()
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON file saved to {json_path}. Time taken: {time.time() - start_time:.2f} seconds.")

def save_to_text(data, output_directory):
    """Save data to a text file."""
    ensure_directory_exists(output_directory)
    text_path = os.path.join(output_directory, "professor_data.txt")
    start_time = time.time()
    with open(text_path, "w") as text_file:
        for entry in data:
            # text_file.write(f"Professor Name: {entry['Professor Name']}\n")
            text_file.write(f"{entry['Main Website']}\n")
            for link in entry['Sub Links']:
                text_file.write(f"{link}\n")
            text_file.write("\n")
    print(f"Text file saved to {text_path}. Time taken: {time.time() - start_time:.2f} seconds.")


def fetch_url_content(url):
    """Fetch the content of a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def convert_html_to_pdf(html_content, output_file):
    """Convert HTML content to a PDF file."""
    try:
        # Specify the path to wkhtmltopdf manually
        config = pdfkit.configuration(wkhtmltopdf=WKHTHMLTOPDF)
        options = {
            'enable-javascript': '',
            'no-stop-slow-scripts': '',  # Prevents timeout if JS is slow
            'javascript-delay': '2000',  # Waits for JavaScript to load
        }

        # Create a PDF from the HTML content and apply the options
        pdfkit.from_string(html_content, output_file, configuration=config, options=options)
        print(os.path.abspath(output_file))  # This will print the absolute path where the file is saved

        print(f"Successfully saved PDF to {output_file}")
    except Exception as e:
        print(f"Error converting HTML to PDF for {output_file}: {e}")

def process_links(input_file, output_directory):
    """Process links from a text file and convert them to PDFs."""
    ensure_directory_exists(output_directory)

    with open(input_file, 'r') as file:
        for line in file:
            url = line.strip()  # Remove leading/trailing whitespace
            if url:
                print(f"Processing {url}...")
                html_content = fetch_url_content(url)
                if html_content:
                    # Generate a unique filename based on the URL
                    output_file = os.path.join(output_directory, re.sub(r'^https?://www.', '', url).replace('/', '_') + '.pdf')
                    convert_html_to_pdf(html_content, output_file)