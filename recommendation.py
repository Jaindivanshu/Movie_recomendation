import streamlit as st
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Load your saved data
movies = joblib.load("movies.pkl")
tfidf_matrix = joblib.load("tfidf_matrix.pkl")

# Recommendation logic
def recommend_movies(title, n=5):
    """Return top n similar movies for the given title."""
    if title not in movies['title'].values:
        return ["Movie not found."]

    idx = movies[movies['title'] == title].index[0]
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-n-1:-1][::-1]
    recommendations = movies.iloc[similar_indices]['title'].tolist()
    return recommendations

# --- NEW FUNCTION ---
api_key = st.secrets["API_KEY"]

def get_movie_info(movie_title):
    """Fetch poster, plot, year, and IMDb rating from OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url).json()

    poster = response.get("Poster", "")
    if not poster or poster == "N/A":
        poster = "https://via.placeholder.com/200x300?text=No+Image"

    plot = response.get("Plot", "No description available.")
    year = response.get("Year", "N/A")
    rating = response.get("imdbRating", "N/A")

    return {
        "poster": poster,
        "plot": plot,
        "year": year,
        "rating": rating
    }
