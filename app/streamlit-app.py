import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from pinecone.grpc import PineconeGRPC as Pinecone
import logging
from preprocessings import load_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone using your API key
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("movie-recommendation-system")

def get_movie_id_by_title(movie_title, data):
    movie_info = data[data['title'] == movie_title].iloc[0]
    movie_id = movie_info['movieId']
    return movie_id

def recommend_movies(movie_title, data, top_k, selected_genres):
    # Get the movie ID for the provided movie title
    movie_id = get_movie_id_by_title(movie_title, data)
    if not movie_id:
        return []

    # Query Pinecone for recommendations
    query_response = index.query(
        id=str(movie_id),
        top_k=top_k + 1,  # +1 to exclude the original movie
        include_metadata=True
    )

    if not query_response or 'matches' not in query_response:
        st.write("No matches found for the movie.")
        return []

    # Collect the recommended movies, skipping the first match (original movie)
    recommended_movies = []
    for match in query_response['matches'][1:top_k + 1]:  # Start from the 2nd item for recommendations
        metadata = match.get('metadata', {})
        movie_id = int(match['id'])  # Convert to integer to match data format
        movie_name = metadata.get('movie_name', 'Unknown Title')
        movie_genre = metadata.get('movie_genre', 'Unknown Genre').split()  # Split genres for comparison
        
        # Check if movie matches any selected genres
        if selected_genres:
            if not set(selected_genres).intersection(movie_genre):
                continue  # Skip if no matching genres

        # Retrieve imdbId from data using movie_id
        imdb_id = data[data['movieId'] == movie_id]['imdbId'].values[0]
        
        recommended_movies.append({
            'movie_id': movie_id,
            'movie_name': movie_name,
            'movie_genre': " ".join(movie_genre),  # Rejoin to display properly
            'imdb_id': imdb_id
        })
    
    return recommended_movies

def get_movie_poster(imdb_id):
    if not imdb_id:
        return ""
    url = f"http://www.omdbapi.com/?i=tt{str(imdb_id).zfill(7)}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', '')

def main():
    st.set_page_config(
        page_title="Movie Recommender",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""<style>
            .title { font-size: 36px; font-weight: bold; color: #333333; text-align: center; margin-bottom: 30px; }
            .movie-card { border: 2px solid #ddd; border-radius: 10px; padding: 10px; background-color: rgba(255, 255, 255, 0.8); text-align: center; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3); transition: transform 0.3s ease-in-out; margin-top: 20px; width: 100%; height: 500px; }
            .movie-card:hover { transform: scale(1.05); }
            .movie-title { font-size: 16px; font-weight: bold; margin-top: 10px; color: #333; }
            .movie-image { width: 100%; border-radius: 8px; height: 400px; object-fit: cover; }
            .movie-genres { font-size: 14px; color: #555; margin-top: 5px; }
        </style>""", unsafe_allow_html=True)

    st.markdown('<div class="title">Movie Recommendation System</div>', unsafe_allow_html=True)

    data = load_data()
    if data is None or data.empty:
        st.write("Error: Data not loaded correctly.")
        return

    movie_title = st.selectbox("Select a Movie", data['title'].values)
    genres_list = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                   'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                   'IMAX', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    selected_genres = [genre for genre in genres_list if st.sidebar.checkbox(genre)]

    if st.button('Recommend'):
        recommended_movies = recommend_movies(movie_title, data, 12, selected_genres)

        if not recommended_movies:
            st.write("No recommendations found.")
        else:
            # Display in a 4x3 grid
            num_columns = 3
            rows = [recommended_movies[i:i + num_columns] for i in range(0, len(recommended_movies), num_columns)]

            for row in rows:
                cols = st.columns(num_columns)
                for col, movie in zip(cols, row):
                    poster_url = get_movie_poster(movie['imdb_id'])
                    with col:
                        st.markdown(f"""
                            <div class="movie-card">
                                <img src="{poster_url}" class="movie-image" />
                                <div class="movie-title">{movie['movie_name']}</div>
                                <div class="movie-genres">Genres: {movie['movie_genre']}</div>
                            </div>
                        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
