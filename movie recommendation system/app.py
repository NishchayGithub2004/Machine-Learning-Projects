import pickle
import streamlit as st
import requests

# create a function to fetch movie poster from API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# create a function to recommend movies by first finding the index of the movie in the list 
# and then finding the similarity of that movie with all the other movies 
# and then sorting the movies based on the similarity through cosine similarity matrix and then returning the top 5 movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

st.header('Movie Recommendation System') # create a header for the app using streamlit

# load the pickle files
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values # create a list of all the movies

selected_movie = st.selectbox("Type or select a movie from the dropdown",movie_list) # create a dropdown for the user to select a movie

if st.button('Show Recommendation'): # if user presses the 'Show Recommendation' button
    # then call the 'recommend' function and store the recommended movie names and posters in two separate lists
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5) # create 5 columns for the recommended movies
    
    # display the recommended movies in the columns using streamlit with their names and posters

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