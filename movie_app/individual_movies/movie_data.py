import streamlit as st
import pandas as pd
import urllib.parse
from .cast_crew_data import display_people_details

def create_person_buttons(names, people_df):
    """Create buttons for names that exist in the people_details database."""
    names_list = names.split(', ')
    buttons = []
    for i in range(0, len(names_list), 5):
        cols = st.columns(5)
        for col, name in zip(cols, names_list[i:i+5]):
            if name in people_df['name'].values:
                if col.button(name, key=f"person_{name}"):
                    st.query_params.update({'person': name, 'scrollTo': 'cast-and-crew-details'})
                    st.rerun()
            else:
                col.write(name)
            buttons.append(name)
    return ' '.join(buttons)

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
        st.markdown(f"<div class='element small-button'>{create_person_buttons(', '.join(movie_details['cast'].split(', ')[:10]) + ', ' + movie_details['directors'], people_df)}</div>", unsafe_allow_html=True)
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

def get_similarity_explanation(movie1, movie2):
    """Generate an explanation of what makes the movies similar."""
    explanations = []

    common_genres = set(movie1['genres'].split(', ')).intersection(set(movie2['genres'].split(', ')))
    if common_genres:
        explanations.append(f"Genres: {', '.join(sorted(common_genres))}")

    common_keywords = set(movie1['keywords'].split(', ')).intersection(set(movie2['keywords'].split(', ')))
    if common_keywords:
        explanations.append(f"Keywords: {', '.join(sorted(common_keywords))}")

    common_directors = set(movie1['directors'].split(', ')).intersection(set(movie2['directors'].split(', ')))
    if common_directors:
        explanations.append(f"Directors: {', '.join(sorted(common_directors))}")

    common_cast = set(movie1['cast'].split(', ')[:8]).intersection(set(movie2['cast'].split(', ')[:8]))
    if common_cast:
        explanations.append(f"Cast: {', '.join(sorted(common_cast))}")

    if movie2['original_title'] in movie1['recommendations']:
        explanations.append("Recommended by the same movie")
    if movie2['original_title'] in movie1['similar_movies']:
        explanations.append("Similar movies")

    return "\n".join(explanations) if explanations else "No significant similarities"

def get_recommendations_by_name(movie_name, df):
    """Get recommendations for a movie based on its name."""
    movie_name = movie_name.split(' (')[0]
    movie = df[df['original_title'].str.contains(movie_name, case=False, na=False)]
    if not movie.empty:
        movie = movie.iloc[0]
        df['similarity'] = df.apply(lambda x: calculate_similarity(movie, x), axis=1)
        recommendations = df.sort_values(by='similarity', ascending=False).head(7)
        recommendations = recommendations[recommendations['original_title'] != movie_name]
        return recommendations
    else:
        return pd.DataFrame()

def calculate_similarity(movie1, movie2):
    """Calculate similarity score between two movies."""
    if pd.notna(movie1['belongs_to_id']) and pd.notna(movie2['belongs_to_id']) and movie1['belongs_to_id'] == movie2['belongs_to_id']:
        return 0

    genre_similarity = jaccard_similarity(movie1['genres'], movie2['genres'])
    keyword_similarity = jaccard_similarity(movie1['keywords'], movie2['keywords'])
    director_similarity = 1 if set(movie1['directors']) == set(movie2['directors']) else 0

    cast1 = movie1['cast'].split(', ')[:8]
    cast2 = movie2['cast'].split(', ')[:8]
    cast_similarity = jaccard_similarity(cast1, cast2)

    extra_points = 0
    if movie2['original_title'] in movie1['recommendations']:
        extra_points += 0.1
    if movie2['original_title'] in movie1['similar_movies']:
        extra_points += 0.1

    similarity_score = (0.4 * genre_similarity +
                        0.3 * keyword_similarity +
                        0.2 * director_similarity +
                        0.1 * cast_similarity +
                        extra_points)

    return similarity_score

def jaccard_similarity(list1, list2):
    """Calculate Jaccard similarity between two lists."""
    intersection = len(set(list1).intersection(set(list2)))
    union = len(set(list1).union(set(list2)))
    return intersection / union if union != 0 else 0

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