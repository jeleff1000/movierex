import streamlit as st
import pandas as pd
import urllib.parse
from .cast_crew_data import display_people_details
from .movie_details import display_movie_details
from .utils import create_person_buttons

def movie_info_tab(df, people_df):
    """Render the movie info tab in Streamlit."""
    st.title('Movie Information')

    # Initialize session state for selected movie
    if 'selected_movie' not in st.session_state:
        st.session_state.selected_movie = ""

    # Get query parameters
    query_params = st.query_params
    movie_from_url = query_params.get('movie', None)
    year_from_url = query_params.get('year', None)

    # Decode the movie title from URL
    if movie_from_url:
        movie_from_url = urllib.parse.unquote(movie_from_url)

    # Create a list of movie titles with years
    all_movie_titles_with_year = [f"{title} ({year})" for title, year in zip(df['original_title'], df['release_year'])]
    all_movie_titles_with_year_sorted = sorted(all_movie_titles_with_year)

    # Dropdown with all movie titles with years
    selected_movie_with_year = st.selectbox("", [""] + all_movie_titles_with_year_sorted,
                                            index=all_movie_titles_with_year_sorted.index(
                                                f"{movie_from_url} ({year_from_url})") + 1 if movie_from_url and year_from_url else 0)

    # Extract the movie title and year from the selected option
    if selected_movie_with_year:
        selected_movie, selected_year = selected_movie_with_year.rsplit(" (", 1)
        selected_year = int(selected_year.rstrip(")"))
    else:
        selected_movie, selected_year = "", None

    # Display selected movie details if a movie is selected
    if selected_movie and selected_year:
        st.session_state.selected_movie = selected_movie
        movie_name = selected_movie.replace(' ', '%20').replace('+', '%2B')
        st.query_params.update({'movie': movie_name, 'year': selected_year})
        display_movie_details(selected_movie, selected_year, df, people_df)

    # Display cast and crew details
    st.markdown("---")
    display_people_details(people_df)