import streamlit as st
import pandas as pd
import os

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full paths to the Parquet files
people_file_path = os.path.join(current_dir, 'people_details.parquet')
movies_file_path = os.path.join(current_dir, 'movies_details.parquet')

# Load the Parquet files
people_df = pd.read_parquet(people_file_path)
movies_df = pd.read_parquet(movies_file_path)

# Import the modules using relative imports
from individual_movies import movie_data
from recommendations import movie_recs

# Create tabs
tab1, tab2 = st.tabs(["Movie Data", "Recommendations"])

with tab1:
    movie_data.movie_info_tab(movies_df, people_df, movies_df)

with tab2:
    movie_recs.recommendations_tab(movies_df)