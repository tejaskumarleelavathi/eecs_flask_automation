import logging  # Import logging module to handle application logs

def get_logger(filename):
    

    # Configure logging: INFO level, log format, and handlers for file and console output
    logging.basicConfig(
        level=logging.INFO,  # Capture messages at INFO level and above
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
        handlers=[
            logging.FileHandler("app.log"),  # Log messages to 'app.log' file
            logging.StreamHandler()  # Also print log messages to the console
        ]
    )

    # Create and return a logger with the specified filename
    logger = logging.getLogger(filename)
    return logger
