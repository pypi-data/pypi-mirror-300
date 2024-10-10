import logging
logger = logging.getLogger()
# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the file handler (or any handler)
file_handler.setFormatter(formatter)