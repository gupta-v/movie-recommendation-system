from dotenv import load_dotenv
import os
from pinecone.grpc import PineconeGRPC as Pinecone
from data_ingestion import load_data

load_dotenv()
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
        print("No matches found for the movie.")
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

def main():

    data = load_data()


    movie_title = input("Enter movie title: ")
    genres_list = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                   'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                   'IMAX', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    selected_genres = []
 
    recommended_movies = recommend_movies(movie_title, data, 12, selected_genres)
    print(recommended_movies)
    
if __name__ == '__main__':
    main()