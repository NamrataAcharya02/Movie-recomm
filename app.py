import streamlit as st
import pickle
import pandas as pd
import numpy as np
import json
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
sim_matrix = pickle.load(open('sim_matrix.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movie_titles = movies['title'].values
#fetch posters
import requests
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=313d472eb369caf6efc743edf446e65f".format(movie_id))
    data = response.json()
    if "poster_path" in data:
        image_path = "https://image.tmdb.org/t/p/original" + data['poster_path']
    else:
        image_path = "https://eagle-sensors.com/wp-content/uploads/unavailable-image.jpg"
    return image_path

#function to recommend movie
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_row = sim_matrix[index]  #contains distances to that movie
    sim_indices = np.argsort(movie_row)[-6:-1]
    sim_indices = sorted(sim_indices, reverse=True)  #indices which correspond to top 5 similar movies
    sim_movies = []
    posters = []
    for i in sim_indices:
        sim_movies.append(movies.iloc[i].title)
        posters.append(fetch_poster(movies.iloc[i].movie_id))
    return sim_movies, posters

st.title("Movie recommender system")
selected_title = st.selectbox("Select or type a movie", movie_titles)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_title)
    col1, col2, col3, col4, col5 = st.columns(5)
    with st.container():
        with col1:
            st.write(recommendations[0])
        with col2:
            st.write(recommendations[1])
        with col3:
            st.write(recommendations[2])
        with col4:
            st.write(recommendations[3])
        with col5:
            st.write(recommendations[4])
    
    col6, col7, col8, col9, col10 = st.columns(5)

    with st.container():
        with col6:
            st.image(posters[0])
        with col7:
            st.image(posters[1])
        with col8:
            st.image(posters[2])
        with col9:
            st.image(posters[3])
        with col10:
            st.image(posters[4])
