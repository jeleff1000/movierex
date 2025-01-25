import streamlit as st
import pandas as pd

# Load the Parquet files
people_df = pd.read_parquet('people_details.parquet')
movies_df = pd.read_parquet('movies_details.parquet')

# Import the modules using relative imports
from individual_movies import movie_data
from recommendations import movie_recs

# Create tabs
tab1, tab2 = st.tabs(["Movie Data", "Recommendations"])

with tab1:
    movie_data.movie_info_tab(movies_df, people_df)

with tab2:
    movie_recs.recommendations_tab(movies_df)