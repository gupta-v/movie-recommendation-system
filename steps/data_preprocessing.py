import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

from data_ingestion import load_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(data, max_features=7000, ngram_range=(1, 2)):
    """
    Preprocesses the movie data to compute cosine similarity based on combined features.
    Uses TF-IDF vectorizer to convert text features into numerical form, and then calculates 
    cosine similarity between movies based on their features.
    
    Args:
    - data (DataFrame): The movie dataset with a 'combined_features' column containing the text.
    - max_features (int, optional): The maximum number of features to extract with the vectorizer. Default is 7000.
    - ngram_range (tuple, optional): The n-gram range for the vectorizer. Default is (1, 2) for unigrams and bigrams.
    
    Returns:
    - cosine_sim (ndarray): Cosine similarity matrix of the movies.
    """
    try:
        logging.info("Data preprocessing started")

        # Check if the necessary column exists
        if 'combined_features' not in data.columns:
            raise ValueError("'combined_features' column is missing from the dataset.")

        # Check for empty dataset
        if data.empty:
            raise ValueError("The dataset is empty.")

        # Log the shape of the input data
        logging.info(f"Input data shape: {data.shape}")

        # Fill empty combined_features with an empty string (if any)
        data['combined_features'].fillna('')

        # Initialize TfidfVectorizer with some enhancements
        vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features, ngram_range=ngram_range)

        logging.info("Fitting TF-IDF Vectorizer...")
        # Fit the vectorizer to the data and transform the combined features column
        tfidf_matrix = vectorizer.fit_transform(data['combined_features'])

        # Log the size of the resulting TF-IDF matrix
        logging.info(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

        logging.info("Calculating cosine similarity...")
        # Compute cosine similarity between the movies
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        logging.info(f"cosine similarity matrix shape: {cosine_sim.shape}")

        logging.info("Data preprocessing completed successfully")
        return cosine_sim,tfidf_matrix

    except Exception as e:
        logging.error(f"Error occurred during preprocessing: {str(e)}")
        raise e
    
def reduce_dimensions(tfidf_matrix, n_components):
    """
    Reduces the dimensionality of the TF-IDF matrix using TruncatedSVD.

    Args:
    - tfidf_matrix (ndarray): The original TF-IDF matrix.
    - n_components (int): Number of dimensions to reduce to.

    Returns:
    - reduced_tfidf_matrix (ndarray): The reduced-dimensional TF-IDF matrix.
    """
    print("Starting dimensionality reduction using TruncatedSVD...")
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    reduced_tfidf_matrix = svd.fit_transform(tfidf_matrix)
    print(f"Dimensionality reduced from {tfidf_matrix.shape[1]} to {n_components} components.")
    return reduced_tfidf_matrix

