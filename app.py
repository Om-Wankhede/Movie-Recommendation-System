import os
import pickle
import streamlit as st
import requests
import gdown

# -----------------------------
# Download similarity.pkl if missing
# -----------------------------
FILE_ID = "1_i-fqj44Xua9SLAg3J2pK7uxstRS7_vu"

if not os.path.exists("similarity.pkl"):
    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        "similarity.pkl",
        quiet=False
    )

# -----------------------------
# TMDB API
# -----------------------------
API_KEY = "722116903b347d5f8825323da60964e3"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    response = requests.get(url)
    data = response.json()

    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

    return "https://via.placeholder.com/500x750?text=No+Poster"

# -----------------------------
# Recommendation Function
# -----------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# -----------------------------
# Load Data
# -----------------------------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = __import__("pandas").DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬")

st.header("🎬 Movie Recommendation System")

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Show Recommendation"):

    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])