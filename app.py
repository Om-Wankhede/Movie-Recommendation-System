<<<<<<< HEAD
import os
import gdown

FILE_ID = "1_i-fqj44Xua9SLAg3J2pK7uxstRS7_vu"

if not os.path.exists("similarity.pkl"):
    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        "similarity.pkl",
        quiet=False
    )




=======
>>>>>>> adef2b5 (updated  commit)
import streamlit as st
import pickle
import pandas as pd
import requests

# Replace with your own TMDB API Key
API_KEY = "722116903b347d5f8825323da60964e3"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    response = requests.get(url)
    data = response.json()

    if 'poster_path' not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    reco_movies = []
    reco_movies_poster = []

    for i in movie_list:
        # Fetch actual TMDB movie_id
        movie_id = movies.iloc[i[0]].movie_id

        reco_movies.append(movies.iloc[i[0]].title)
        reco_movies_poster.append(fetch_poster(movie_id))

    return reco_movies, reco_movies_poster


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])