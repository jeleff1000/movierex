import pandas as pd

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