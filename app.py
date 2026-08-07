import os
import gdown
import streamlit as st
import pickle
import pandas as pd
import requests

# -----------------------------
# Google Drive File ID
# -----------------------------
FILE_ID = "1_i-fqj44Xua9SLAg3J2pK7uxstRS7_vu"

# Download similarity.pkl only once
if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl...")
    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        "similarity.pkl",
        quiet=False
    )

# -----------------------------
# TMDB API Key
# -----------------------------
API_KEY = "YOUR_TMDB_API_KEY"   # Replace with your API key

# -----------------------------
# Load Data (cached)
# -----------------------------
@st.cache_resource
def load_similarity():
    with open("similarity.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_movies():
    with open("movies_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)
    return pd.DataFrame(movies_dict)

similarity = load_similarity()
movies = load_movies()

# -----------------------------
# Fetch Poster
# -----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    response = requests.get(url)
    data = response.json()

    if data.get("poster_path") is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    reco_movies = []
    reco_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        reco_movies.append(movies.iloc[i[0]].title)
        reco_posters.append(fetch_poster(movie_id))

    return reco_movies, reco_posters

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])