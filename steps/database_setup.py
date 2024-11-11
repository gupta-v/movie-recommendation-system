import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from data_ingestion import load_data
from data_preprocessing import preprocess_data
from data_preprocessing import reduce_dimensions



load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
# Initialize Pinecone with your API key

pc = Pinecone(api_key=PINECONE_API_KEY)

# Create a connection to the Pinecone index
index = pc.Index("movie-recommendation-system")  # Your Pinecone index name


def upsert_tfidf_vectors_to_pinecone(data, reduced_tfidf_matrix, chunk_size=1000):
    """
    Upserts the reduced TF-IDF vectors into Pinecone index.

    Args:
    - data (DataFrame): The movie dataset.
    - reduced_tfidf_matrix (ndarray): The reduced TF-IDF matrix representing the movies.
    - chunk_size (int): The number of vectors per batch (max 1000 as per Pinecone).
    """
    try:
        total_rows = reduced_tfidf_matrix.shape[0]
        upsert_data = []

        for i in range(total_rows):
            # Extract movie ID and vector
            movie_id = str(data['movieId'].iloc[i])
            reduced_vector = reduced_tfidf_matrix[i].tolist()  # Reduced-dimensional vector

            # Prepare data for upsert
            upsert_data.append({
                "id": movie_id,
                "values": reduced_vector,
                "metadata": { "movie_name": data['title'].iloc[i],
                             "movie_genre": data['genres'].iloc[i]}
            })

            # Perform batch upsert when chunk is ready
            if (i + 1) % chunk_size == 0 or (i + 1) == total_rows:
                index.upsert(vectors=upsert_data)
                upsert_data = []  # Clear the list for the next batch
                print(f"Upserted {i + 1}/{total_rows} vectors")

        print("Upsert completed successfully to Pinecone!")

    except Exception as e:
        print(f"Error occurred during upsert: {str(e)}")
        raise e

# Load and preprocess the data
data = load_data()
if data is None or data.empty:
    raise ValueError("Loaded data is empty or None.")

# Preprocess data and get TF-IDF matrix
cosine_sim, tfidf_matrix = preprocess_data(data)

# Reduce dimensionality of the TF-IDF matrix
reduced_tfidf_matrix = reduce_dimensions(tfidf_matrix, n_components=500)

# Upsert the reduced TF-IDF data into the Pinecone index
upsert_tfidf_vectors_to_pinecone(data, reduced_tfidf_matrix)
