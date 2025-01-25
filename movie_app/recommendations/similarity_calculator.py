import pandas as pd

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