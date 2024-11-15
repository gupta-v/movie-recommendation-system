# Movie Recommendation System

This is a **Movie Recommendation System** built with content-based filtering and hosted on [Render](https://movie-recommender-zeic.onrender.com/). The system leverages metadata such as movie genres, titles, and tags to recommend movies based on similarity. The recommendation engine uses **Pinecone** for vector similarity search and **TF-IDF** vectorization for feature extraction.

## Table of Contents

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Uses and Scope](#uses-and-scope)
- [File Structure](#file-structure)
- [Software and Tools Requirements](#software-and-tools-requirements)
- [Getting Started](#getting-started)
- [Data Description](#data-description)
- [Usage](#usage)
- [Project Steps](#project-steps)
  - [1. Data Ingestion](#1-data-ingestion)
  - [2. Data Preprocessing](#2-data-preprocessing)
  - [3. Database Setup ](#3-database-setup)
  - [4. Model](#4-model)
  - [5. Model Evaluation](#model-evaluation)
- [Future Enhancements](#future-enhancements)
- [Hosted Link](#hosted-link)
- [Acknowledgments](#acknowledgments)

## Project Overview

The **Movie Recommendation System** takes a user-selected movie and recommends similar movies by analyzing metadata like genres and keywords. The system uses content-based filtering, where movies with similar features (genre, actors, plot) are recommended. The system allows filtering by genres, making it more customized to users' preferences.

The application uses **Streamlit** for the front-end interface and **Pinecone** for fast vector-based similarity search.

## Features

- **Movie Recommendations**: Get personalized recommendations based on selected movies.
- **Genre Filter**: Users can filter recommendations by genre to receive more relevant suggestions.
- **Interactive UI**: A user-friendly interface with Streamlit to browse and explore movies.
- **Poster Display**: Movie posters are fetched from the OMDB API for better visualization of results.
- **Deployed Live**: Access the live version [here](https://movie-recommender-zeic.onrender.com/).

## Uses and Scope

The Movie Recommendation System offers an intuitive platform for users to discover personalized movie suggestions, while also providing potential for future enhancements:

- Personalized Movie Recommendations: Users can input their favorite movie titles and receive tailored recommendations based on similar genres and metadata, enhancing their movie-watching experience.

- Interactive Genre Filtering: The system allows users to filter recommendations by selecting genres like Action, Comedy, or Sci-Fi, enabling more precise discovery of movies that match their preferences.

- Content-Based Filtering: By analyzing movie metadata, the system delivers recommendations closely aligned with the content and characteristics of previously watched movies, ensuring relevance in suggestions.

- Expansion to Collaborative Filtering: Future iterations could integrate collaborative filtering, allowing recommendations based on user behavior and preferences, enhancing the accuracy and diversity of suggestions.

- Integration with Additional Movie Databases: Incorporating more movie sources such as IMDb or TMDb would enrich the dataset, improving both the variety and accuracy of recommendations.

- Real-Time Feedback and Learning: The system could be expanded to collect real-time feedback (e.g., likes/dislikes), enabling dynamic learning and more personalized recommendations over time.

## File Structure

```plaintext
movie-recommendation-system
│
├── app
│   ├── streamlit-app.py                         # Streamlit application script
│   └── preprocessings.py                        # Preprocessing functions used in Streamlit App
│
├── data
│   └── content_based_filtering_dataset.csv      # Dataset for content-based filtering
│
├── steps
│   ├── data_ingestion.py                        # Script for loading data
│   ├── data_preprocessing.py                    # Script for data preprocessing
│   ├── database_setup.py                        # Script for Pinecone setup and vectorizing Index
│   └── model.py                                 # Script for recommendation engine implementation
│
├── .env.example                                 # Example environment variables file
├── .gitignore                                   # Files and directories to be ignored by Git
├── requirements.txt                             # Python dependencies
└── README.md                                    # Project documentation
```

## Software and Tools Requirements

1. [GitHub Account](https://github.com/)
2. [Render Account](https://render.com/)
3. [Pinecone Account](https://www.pinecone.io/)
4. [OMDB API](https://www.omdbapi.com/apikey.aspx?__EVENTTARGET=freeAcct&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKLTIwNDY4MTIzNQ9kFgYCAQ9kFgICBw8WAh4HVmlzaWJsZWhkAgIPFgIfAGhkAgMPFgIfAGhkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYDBQtwYXRyZW9uQWNjdAUIZnJlZUFjY3QFCGZyZWVBY2N0oCxKYG7xaZwy2ktIrVmWGdWzxj%2FDhHQaAqqFYTiRTDE%3D&__VIEWSTATEGENERATOR=5E550F58&__EVENTVALIDATION=%2FwEdAAU%2BO86JjTqdg0yhuGR2tBukmSzhXfnlWWVdWIamVouVTzfZJuQDpLVS6HZFWq5fYpioiDjxFjSdCQfbG0SWduXFd8BcWGH1ot0k0SO7CfuulHLL4j%2B3qCcW3ReXhfb4KKsSs3zlQ%2B48KY6Qzm7wzZbR&at=freeAcct&Email=)
5. [Python 3](https://www.python.org/downloads/)
6. [VSCode IDE](https://code.visualstudio.com/)
7. [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-The-Command-Line)

## Getting Started

### Prerequisites

- **Python**: Version 3.7 or higher
- **pip**: Ensure `pip` is installed for managing project dependencies

### Installation

- Clone the repository:

  ```sh
  git clone https://github.com/gupta-v/movie-recommendation-system.git

  ```

- Navigate to the project directory:

  ```sh
  cd movie-recommendation-system

  ```

- Install the required packages using requirements.txt:

  ```sh
  pip install -r requirements.txt
  ```

- Set up your environment variables:

  ```sh
  cp .env.example .env

  ```

  Edit the .env file with the necessary details

  - (API keys for OMDB, Pinecone, etc.).

## Data Description

The dataset used for content-based filtering includes movie metadata such as titles, genres, tags, relevant tags , combined data and movie IDs. The dataset is loaded from content_based_filtering_dataset.csv located in the data/ folder.

Key columns:

- movieId: Unique ID for each movie.
- title: The name of the movie.
- genres: List of genres the movie belongs to.
- tag: List of tags given to the movies.
- relevant_tags: List of tags that are relevant according to users.
- combined_features: This column contains the string of all genres, tags & relevant_tags for each movie row.
- imdbId: The IMDb ID used to fetch movie posters.

## Usage

- Create a Pinecone Index:

  - Visit [Pinecone.io](https://www.pinecone.io/) and create an index for your data vectors.
  - Create the index with -
  - **Index Name** : movie-recommendation-system
  - **Dimension** : 500
  - **Metric** : Cosine

- Run the following Script to setup the index with your data vectors in Pinecone:

  ```sh
  python .\steps\database_setup.py
  ```

- Start the Streamlit app:

  ```sh
  streamlit run app/streamlit-app.py

  ```

## Project Steps

### 1. Data Ingestion:

- Script: data_ingestion.py
- Description: Loads the movie metadata from data/content_bases_filtering_dataset using pandas and logs the data loading process.

### 2. Data Preprocessing:

- Script: data_preprocessing.py
- Description: Prepossesses the data by embedding / vectoring the combined_features. Calculating TFidf Vector and cosine metric for the same. Also reduces the dimension of the Tfidf vector so that it could be use without any memory error in any vector database.

### 3. Database Setup:

- Script: database_setup.py
- Description: Setting up the pinecone vector database to use cosine metric for recommendations.

### 4. Model:

- Script: model.py
- Description: Model contains recommend function and more processing used to call pinecone api and queries the index for recommendations.

### Model Evaluation

- Metrics Used:
  - Cosine Similarity
  - Recommend top 12 matching movie with respect to movie title given.

## Future Enhancements

### Scalability:

- Distributed Pinecone Setup: As more data is added, Pinecone's distributed architecture allows for seamless scaling of vector similarity search.
- Expanding Dataset: Integrating more features like actor names, director names, and plot keywords could improve recommendation quality.
- Hybrid Recommendation System: Future iterations could combine content-based filtering with collaborative filtering techniques (such as using user ratings) for better accuracy.

### Possible Features:

- User Profiles: Implementing user profiles to provide personalized recommendations based on past behavior.
- Collaborative Filtering: Add collaborative filtering to include recommendations based on similar users’ tastes.
  More Customization: Adding more filters (e.g., release year, popularity) to fine-tune recommendations.

## Hosted Link

- The project is deployed on Render, and it is accessible at https://movie-recommender-zeic.onrender.com/.

- Render handles automatic deployments for every new push to the repository, ensuring the app stays up-to-date.

## Acknowledgments

- Inspired by the diversity and enthusiasm of movie lovers who explore the vast world of **Entertainment**.
- Grateful to the open-source community for providing the tools, libraries, and resources that made this project possible.
