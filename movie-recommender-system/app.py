import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=9edef0cd5c3f1929894cfa66e4abc2a2&language=en-US '
                            .format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  # poster path has the url of poster


movies = pickle.load(open('movies.pkl', 'rb'))  # This contains the new_df file of jupyter notebook
movies_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movie = []
    recommended_movie_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id  # Using movie_id to fetch poster from tmdb API
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movie, recommended_movie_poster


st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Enter Movie Name', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)  # Creating a function which will recommend movies

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])
    with col6:
        st.header(names[5])
        st.image(posters[5])
