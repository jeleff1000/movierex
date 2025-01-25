# utils.py
import streamlit as st
from .similarity import get_similarity_explanation  # Import the function

def create_person_dropdown(names, people_df):
    """Create a dropdown menu for names that exist in the people_details database."""
    names_list = names.split(', ')
    filtered_names = [name for name in names_list if name in people_df['name'].values]

    if filtered_names:
        options = ["Select a person"] + filtered_names
        selected_name = st.selectbox("", options)
        if selected_name != "Select a person":
            st.query_params.update({'person': selected_name})
            # Use JavaScript to append the hashtag to the URL
            st.write(f'<script>window.location.href = window.location.href.split("?")[0] + "?" + new URLSearchParams(window.location.search) + "#cast-and-crew-details";</script>', unsafe_allow_html=True)
    return ''

def create_movie_buttons(recommendations, movie_details):
    """Create buttons for recommended movies."""
    all_cols = st.columns(min(len(recommendations), 5))
    for col, (_, movie) in zip(all_cols, recommendations.head(5).iterrows()):
        with col:
            col.markdown(f"<div class='center-content'><div class='element one-line-title'>{movie['original_title']}</div><div class='year'>{movie['release_year']}</div></div>", unsafe_allow_html=True)
            col.image(movie['poster_path'], use_container_width=True)
            col.markdown('<div class="center-content">', unsafe_allow_html=True)
            if col.button("Select", key=f"select_{movie['id']}"):
                st.session_state.selected_movie = movie['original_title']
                movie_name = movie['original_title'].replace(' ', '%20').replace('+', '%2B')
                st.query_params.update({'movie': movie_name, 'year': movie['release_year']})
                st.write('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
            col.markdown('</div>', unsafe_allow_html=True)
            similarity_explanation = get_similarity_explanation(movie_details, movie)
            with col.expander("Similarities"):
                col.markdown(f"<div class='element'>{similarity_explanation}</div>", unsafe_allow_html=True)

def create_movie_dropdown(movies, person_details):
    """Create a dropdown menu for movies."""
    actor_name = person_details['name']
    matched_movies = movies[movies['cast'].str.contains(actor_name, na=False)]

    if matched_movies.empty:
        st.error(f"No movies found for actor: {actor_name}")
        return
    movie_names = [f"{movie['original_title']} ({movie['release_year']})" for _, movie in matched_movies.iterrows()]
    options = ["Select a movie"] + movie_names
    selected_movie = st.selectbox("", options)
    if selected_movie != "Select a movie":
        movie_title, movie_year = selected_movie.rsplit(' (', 1)
        movie_year = movie_year.rstrip(')')
        movie = matched_movies[(matched_movies['original_title'] == movie_title) & (matched_movies['release_year'] == int(movie_year))].iloc[0]
        movie_name = movie['original_title'].replace(' ', '%20').replace('+', '%2B')
        st.query_params.update({'movie': movie_name, 'year': movie['release_year']})
        st.write('<script>window.scrollTo(0, 0);</script>', unsafe_allow_html=True)
    return ''