import streamlit as st
import pandas as pd
from .similarity_calculator import calculate_similarity
from .input_file import upload_file

# Function to get recommendations based on selected movie IDs
def get_recommendations_by_ids(movie_ids, min_rating, max_rating, df, language_filter, runtime_max, release_year_range, genre_filters):
    """Get recommendations for multiple movies based on their IDs and various filters."""
    selected_movies = df[df['id'].isin(movie_ids)]
    if not selected_movies.empty:
        df['similarity'] = df.apply(lambda x: sum(calculate_similarity(movie, x) for _, movie in selected_movies.iterrows()), axis=1)
        recommendations = df.sort_values(by='similarity', ascending=False)
        recommendations = recommendations[(recommendations['vote_average'] >= min_rating) & (recommendations['vote_average'] <= max_rating)]
        recommendations = recommendations[recommendations['spoken_languages'].str.contains(language_filter, case=False, na=False)]
        recommendations = recommendations[df['runtime'] <= runtime_max]
        recommendations = recommendations[(recommendations['release_year'] >= release_year_range[0]) & (recommendations['release_year'] <= release_year_range[1])]
        if genre_filters:
            recommendations = recommendations[recommendations['genres'].apply(lambda x: all(genre in x for genre in genre_filters))]
        recommendations = recommendations[~((recommendations['vote_average'] > 6.5) & (recommendations['vote_count'] < 500))]
        recommendations = recommendations.head(7)
        recommendations = recommendations[~recommendations['id'].isin(movie_ids)]
        return recommendations
    else:
        return pd.DataFrame()

# Streamlit app to display the recommendations
def recommendations_tab(df):
    """Render the recommendations tab in Streamlit."""
    st.title('Movie Recommendations')

    all_movie_titles_with_year = [f"{title} ({year})" for title, year in zip(df['original_title'], df['release_year'])]
    all_movie_ids = df['id'].tolist()
    movie_options = {f"{title} ({year})": movie_id for title, year, movie_id in zip(df['original_title'], df['release_year'], all_movie_ids)}

    # Get query parameters
    query_params = st.query_params
    selected_movies = query_params.get_all('movies') or []

    # Ensure at least 4 select boxes
    while len(selected_movies) < 4:
        selected_movies.append("")

    # Create select boxes dynamically based on the number of selected movies
    rows = [st.columns(2) for _ in range((len(selected_movies) + 1) // 2)]
    for i in range(len(selected_movies)):
        with rows[i // 2][i % 2]:
            options = [""] + list(movie_options.keys())
            index = 0 if i >= len(selected_movies) else options.index(selected_movies[i])
            selected_movie = st.selectbox(f"Selected Movie {i+1}:", options, index=index)
            if selected_movie and selected_movie != "":
                selected_movies[i] = selected_movie

    # Add new movie and clear all buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Movie"):
            selected_movies.append("")
            st.query_params.update(movies=selected_movies)
            st.rerun()
    with col2:
        if st.button("Clear all"):
            st.query_params.clear()
            st.rerun()

    with st.expander("Select Filters"):
        # Slider for vote_average filter
        min_rating, max_rating = st.slider("Select Voter Score Range:", 0.0, 10.0, (0.0, 10.0), step=0.1)

        # Search bar for spoken_languages
        language_filter = st.text_input("Search by Language:")

        # Number input for maximum runtime
        runtime_max = st.number_input("Select Maximum Runtime (minutes):", min_value=0, max_value=300, value=300, step=1)

        # Toggle range for release_year
        release_year_range = st.slider("Select Release Year Range:", int(df['release_year'].min()), int(df['release_year'].max()), (int(df['release_year'].min()), int(df['release_year'].max())), step=1)

        # Multiselect for genre
        genre_options = df['genres'].str.split(', ').explode().unique()
        genre_filters = st.multiselect("Select Genres:", options=genre_options)

    # Update query parameters
    if selected_movies:
        st.query_params.update(movies=selected_movies)

    if selected_movies:
        selected_movie_ids = [movie_options[movie] for movie in selected_movies if movie]
        st.write("Top Recommendations:")
        recommendations = get_recommendations_by_ids(selected_movie_ids, min_rating, max_rating, df, language_filter, runtime_max, release_year_range, genre_filters)
        if not recommendations.empty:
            rows = [st.columns(3) for _ in range(2)]
            for i, (_, movie) in enumerate(recommendations.head(6).iterrows()):
                with rows[i // 3][i % 3]:
                    if st.button(f"**{movie['original_title']} ({movie['release_year']})**", key=f"title_{movie['id']}"):
                        # Find the first empty select box
                        empty_index = next((index for index, value in enumerate(selected_movies) if value == ""), len(selected_movies))
                        if empty_index < len(selected_movies):
                            selected_movies[empty_index] = f"{movie['original_title']} ({movie['release_year']})"
                        else:
                            selected_movies.append(f"{movie['original_title']} ({movie['release_year']})")
                        st.query_params.update(movies=selected_movies)
                        st.rerun()

                    st.image(movie['poster_path'], width=150)
                    st.write(f"{movie['runtime']} min | Rating: {movie['vote_average']:.2f}")

    # File uploader at the bottom
    uploaded_entries = upload_file(movie_options)
    if uploaded_entries:
        selected_movies.extend(uploaded_entries)