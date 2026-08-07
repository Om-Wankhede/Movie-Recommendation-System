import os
import pickle
import random
import requests
import pandas as pd
import streamlit as st
import gdown

FILE_ID = "1_i-fqj44Xua9SLAg3J2pK7uxstRS7_vu"
API_KEY = "722116903b347d5f8825323da60964e3"

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

if not os.path.exists("similarity.pkl"):
    with st.spinner("Downloading recommendation model..."):
        gdown.download(
            f"https://drive.google.com/uc?id={FILE_ID}",
            "similarity.pkl",
            quiet=False,
        )

@st.cache_data
def load_movies():
    with open("movies_dict.pkl","rb") as f:
        return pd.DataFrame(pickle.load(f))

@st.cache_resource
def load_similarity():
    with open("similarity.pkl","rb") as f:
        return pickle.load(f)

movies = load_movies()
similarity = load_similarity()

def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=10).json()
        poster = (
            "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            if data.get("poster_path")
            else "https://via.placeholder.com/300x450?text=No+Poster"
        )
        return poster, data.get("overview","No overview available."), data.get("vote_average","-")
    except Exception:
        return "https://via.placeholder.com/300x450?text=No+Poster","Unable to fetch details.","-"

def recommend(title):
    idx = movies[movies["title"]==title].index[0]
    distances = similarity[idx]
    rec = sorted(list(enumerate(distances)), key=lambda x:x[1], reverse=True)[1:6]
    names, posters = [], []
    for i,_ in rec:
        names.append(movies.iloc[i]["title"])
        posters.append(fetch_details(movies.iloc[i]["movie_id"])[0])
    return names, posters

st.title("🎬 Movie Recommendation System")

selected = st.selectbox("Search Movie", movies["title"].values)

movie_row = movies[movies["title"]==selected].iloc[0]
poster, overview, rating = fetch_details(movie_row["movie_id"])

c1,c2 = st.columns([1,2])
with c1:
    st.image(poster, use_container_width=True)
with c2:
    st.subheader(selected)
    st.write(f"⭐ Rating: {rating}")
    st.write(overview)

st.markdown("### 🎲 Random Movies")
cols = st.columns(5)
sample = movies.sample(5, random_state=random.randint(0,100000))
for col, (_, row) in zip(cols, sample.iterrows()):
    p,_,_ = fetch_details(row["movie_id"])
    with col:
        st.image(p, use_container_width=True)
        st.caption(row["title"])

if st.button("Recommend Similar Movies"):
    with st.spinner("Finding recommendations..."):
        names, posters = recommend(selected)

    st.markdown("## Recommended Movies")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])