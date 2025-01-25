import pandas as pd
import streamlit as st

# Function to calculate Jaccard similarity score
def jaccard_similarity(list1, list2):
    """Calculate Jaccard similarity between two lists."""
    set1, set2 = set(list1), set(list2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Function to calculate similarity score between two movies
def calculate_similarity(movie1, movie2):
    """Calculate similarity score between two movies."""
    if movie1['id'] == movie2['id'] or (pd.notna(movie1['belongs_to_id']) and pd.notna(movie2['belongs_to_id']) and movie1['belongs_to_id'] == movie2['belongs_to_id']):
        return -1_000_000

    genre_similarity = jaccard_similarity(movie1['genres'].split(', '), movie2['genres'].split(', '))
    keyword_similarity = jaccard_similarity(movie1['keywords'].split(', '), movie2['keywords'].split(', '))
    director_similarity = 1 if set(movie1['directors'].split(', ')) == set(movie2['directors'].split(', ')) else 0
    cast_similarity = jaccard_similarity(movie1['cast'].split(', ')[:8], movie2['cast'].split(', ')[:8])
    language_similarity = jaccard_similarity(movie1['spoken_languages'].split(', '), movie2['spoken_languages'].split(', '))

    extra_points = 0
    if movie2['original_title'] in movie1['recommendations']:
        extra_points += 0.1
    if movie2['original_title'] in movie1['similar_movies']:
        extra_points += 0.1

    similarity_score = (0.3 * genre_similarity +
                        0.2 * keyword_similarity +
                        0.2 * director_similarity +
                        0.1 * cast_similarity +
                        0.1 * language_similarity +
                        extra_points)

    return similarity_score

# Function to get recommendations based on selected movie IDs
def get_recommendations_by_ids(movie_ids, min_rating, max_rating, df):
    """Get recommendations for multiple movies based on their IDs and rating filter."""
    selected_movies = df[df['id'].isin(movie_ids)]
    if not selected_movies.empty:
        df['similarity'] = df.apply(lambda x: sum(calculate_similarity(movie, x) for _, movie in selected_movies.iterrows()), axis=1)
        recommendations = df.sort_values(by='similarity', ascending=False)
        recommendations = recommendations[(recommendations['vote_average'] >= min_rating) & (recommendations['vote_average'] <= max_rating)]
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
    selected_movies = query_params.get_all('movies')

    # Multiselect with all movie titles with years
    selected_movies = st.multiselect("Select movies:", list(movie_options.keys()), default=selected_movies)

    # Slider for vote_average filter
    min_rating, max_rating = st.slider("Select Voter Score Range:", 0.0, 10.0, (0.0, 10.0), step=0.1)

    # Clear all button
    if st.button("Clear all"):
        st.query_params.clear()
        st.rerun()

    # Update query parameters
    if selected_movies:
        st.query_params.movies = selected_movies

    if selected_movies:
        selected_movie_ids = [movie_options[movie] for movie in selected_movies]
        st.write("Top Recommendations:")
        recommendations = get_recommendations_by_ids(selected_movie_ids, min_rating, max_rating, df)
        if not recommendations.empty:
            rows = [st.columns(3) for _ in range(2)]
            for i, (_, movie) in enumerate(recommendations.head(6).iterrows()):
                with rows[i // 3][i % 3]:
                    if st.button(f"**{movie['original_title']} ({movie['release_year']})**", key=f"title_{movie['id']}"):
                        st.query_params.movies = selected_movies + [f"{movie['original_title']} ({movie['release_year']})"]
                        st.rerun()
                    st.image(movie['poster_path'], width=150)
                    st.write(f"{movie['runtime']} min | Rating: {movie['vote_average']:.2f}")

if __name__ == "__main__":
    # Load the Parquet file
    movies_df = pd.read_parquet('movies_details.parquet')
    recommendations_tab(movies_df)