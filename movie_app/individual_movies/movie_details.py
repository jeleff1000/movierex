import streamlit as st
import pandas as pd
from .similarity import calculate_similarity, get_similarity_explanation, get_recommendations_by_name
from .utils import create_person_buttons

def display_movie_details(movie_title, movie_year, df, people_df):
    """Display the details of the selected movie."""
    movie_details = df[(df['original_title'].str.lower() == movie_title.lower()) & (df['release_year'] == movie_year)]
    if movie_details.empty:
        st.error("Movie details not found.")
        return
    movie_details = movie_details.iloc[0]

    # Create two columns
    col1, col2 = st.columns([1, 3])

    # Display tagline and poster in the first column
    with col1:
        st.image(movie_details['poster_path'], use_container_width=True)
        st.markdown(f"<p style='font-size:10px;'>{movie_details['tagline']}</p>", unsafe_allow_html=True)

    # Display movie details in the second column
    with col2:
        # Custom CSS to style headers and elements
        st.markdown(
            """
            <style>
            .tiny-header {
                font-size: 12px;
                font-weight: bold;
                margin-bottom: 0.1rem;
            }
            .element {
                font-size: 14px;
                margin-bottom: 0.5rem;
            }
            .small-button button {
                font-size: 8px !important;
                padding: 2px 5px !important;
            }
            .center-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
            .one-line-title {
                display: -webkit-box;
                -webkit-line-clamp: 1;
                -webkit-box-orient: vertical;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .year {
                font-size: 12px;
                color: gray;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Row 1: Title, Runtime, Rating
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        row1_col1.markdown("<div class='tiny-header'>Title</div>", unsafe_allow_html=True)
        row1_col2.markdown("<div class='tiny-header'>Runtime</div>", unsafe_allow_html=True)
        row1_col3.markdown("<div class='tiny-header'>Rating</div>", unsafe_allow_html=True)
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        row2_col1.markdown(f"<div class='element'>{movie_details['original_title']}</div>", unsafe_allow_html=True)
        row2_col2.markdown(f"<div class='element'>{movie_details['runtime']} minutes</div>", unsafe_allow_html=True)
        row2_col3.markdown(f"<div class='element'>{movie_details['vote_average']}</div>", unsafe_allow_html=True)

        # Row 2: Genres, Release Year, Spoken Languages
        row3_col1, row3_col2, row3_col3 = st.columns(3)
        row3_col1.markdown("<div class='tiny-header'>Genres</div>", unsafe_allow_html=True)
        row3_col2.markdown("<div class='tiny-header'>Release Year</div>", unsafe_allow_html=True)
        row3_col3.markdown("<div class='tiny-header'>Spoken Languages</div>", unsafe_allow_html=True)
        row4_col1, row4_col2, row4_col3 = st.columns(3)
        row4_col1.markdown(f"<div class='element'>{movie_details['genres']}</div>", unsafe_allow_html=True)
        row4_col2.markdown(f"<div class='element'>{movie_details['release_year']}</div>", unsafe_allow_html=True)
        row4_col3.markdown(f"<div class='element'>{movie_details['spoken_languages']}</div>", unsafe_allow_html=True)

        # Row 3: Budget, Revenue, Directors
        row5_col1, row5_col2, row5_col3 = st.columns(3)
        row5_col1.markdown("<div class='tiny-header'>Budget</div>", unsafe_allow_html=True)
        row5_col2.markdown("<div class='tiny-header'>Revenue</div>", unsafe_allow_html=True)
        row5_col3.markdown("<div class='tiny-header'>Directors</div>", unsafe_allow_html=True)
        row6_col1, row6_col2, row6_col3 = st.columns(3)
        row6_col1.markdown(f"<div class='element'>{movie_details['budget']}</div>", unsafe_allow_html=True)
        row6_col2.markdown(f"<div class='element'>{movie_details['revenue']}</div>", unsafe_allow_html=True)
        row6_col3.markdown(f"<div class='element'>{movie_details['directors']}</div>", unsafe_allow_html=True)

        # Row 4: Cast and Overview
        st.markdown("<div class='tiny-header'>Cast and Overview</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='element small-button'>{create_person_buttons(', '.join(movie_details['cast'].split(', ')[:8]) + ', ' + movie_details['directors'], people_df)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='element'>{movie_details['overview']}</div>", unsafe_allow_html=True)

    # Row 5: Trailer
    st.markdown("<div class='tiny-header'>Trailer</div>", unsafe_allow_html=True)
    st.video(movie_details['trailers'])

    # Row 6: Recommendations and Similar Movies
    st.markdown("<div class='tiny-header'>Recommendations and Similar Movies</div>", unsafe_allow_html=True)
    recommendations = get_recommendations_by_name(movie_details['original_title'], df)
    if not recommendations.empty:
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
                    st.rerun()
                col.markdown('</div>', unsafe_allow_html=True)
                similarity_explanation = get_similarity_explanation(movie_details, movie)
                with col.expander("Similarities"):
                    col.markdown(f"<div class='element'>{similarity_explanation}</div>", unsafe_allow_html=True)