import pandas as pd
import logging
import sys
import traceback as tb  

# Configure logging
logging.basicConfig(
    filename='data_processor.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DataProcessor:
    """
    A class to handle reading and processing of Excel files containing research data.
    """

    def __init__(self, file_path: str):
        """
        Initializes the DataProcessor with the given file path.
        
        """
        self.file_path = file_path
        self.data = None
        logging.info(f"DataProcessor initialized with file path: {file_path}")

    def read_file(self) -> bool:
        """
        Reads the Excel file and logs any errors encountered.
        
        """
        try:
            self.data = pd.read_excel(self.file_path, header=0)
            logging.info(f"Successfully read the Excel file: {self.file_path}")
            return True
        except:
            # Log the error message and traceback
            logging.error(f"An error occurred while reading the Excel file: {tb.format_exc()}")
            # logging.error(tb.format_exc())
            return False

    def process_data(self) -> pd.DataFrame:
        
        """
        Processes the data by adding headers and formatting research areas.
        
        """
        if self.data is not None:
            try:
                self.data.columns = ['Professor Name', 'University Website', 'Research Website', 'Research Groups']
                self.data['Research Groups'] = self.data['Research Groups'].str.split('\n')
                self.data['Research Groups'] = self.data['Research Groups'].apply(
                    lambda areas: [area.strip().lower() for area in areas] if isinstance(areas, list) else []
                )
                # Flatten the research groups and count occurrences
                all_groups = self.data.explode('Research Groups')['Research Groups']
                #   print(all_groups)
                group_counts = all_groups.value_counts().reset_index()
                group_counts.columns = ['Research Group', 'Number of Professors']
                print(group_counts)
          
            except:
                logging.error(tb.format_exc())
        else:
            logging.warning("No data to process. Ensure the file is read successfully first.")
            return None

    def save_to_excel(self, output_path: str) -> None:
        """
        Saves the processed data to a CSV file.
        
        """
        if self.data is  not None:
            try:
                self.data.to_excel(output_path, index=False)
                logging.info(f"Processed data saved to {output_path}")
            except:
                logging.error(tb.format_exc())

        else:
            logging.warning("No data to save. Ensure the data is processed before saving.")

    def get_professor_websites(self) -> list:
        """
        Returns a list of tuples with professor names and their research websites.
        """
        if self.data is not None:
            try:
                # Filter rows where 'Research Website' is not null, then convert to list of tuples
                professor_websites = self.data[['Professor Name', 'Research Website']].dropna(subset=['Research Website']).to_records(index=False)
                professor_websites = list(professor_websites)
                logging.info("Successfully extracted professor websites.")
                return professor_websites
            except Exception as e:
                logging.error(f"An error occurred while extracting professor websites: {e}")
                logging.error(tb.format_exc())
                return []
        else:
            logging.warning("No data to extract professor websites from.")
            return []
