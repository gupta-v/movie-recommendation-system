import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path="./data/content_based_filtering_dataset.csv"):
    """
    Loads movie data from the specified CSV file path.

    Args:
    - file_path (str): Path to the CSV file containing the movie data. Default is './data/content_based_dataset.csv'.
    
    Returns:
    - data (DataFrame): The loaded movie dataset.
    """
    try:
        logging.info(f"Data Loading Started from {file_path}")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} was not found.")

        # Load the CSV data into a DataFrame
        data = pd.read_csv(file_path, low_memory=False)

        # Check if data is empty after loading
        if data.empty:
            raise ValueError(f"The file {file_path} was loaded but it is empty.")

        logging.info(f"Data Loaded Successfully! Shape of the dataset: {data.shape}")
        return data

    except FileNotFoundError as fnf_error:
        logging.error(f"FileNotFoundError: {str(fnf_error)}")
        return None
    except ValueError as value_error:
        logging.error(f"ValueError: {str(value_error)}")
        return None
    except Exception as e:
        logging.exception("An error occurred while loading the data.")
        return None
