import streamlit as st
import pandas as pd
from .display import recommendations_tab

# Load the Parquet file
try:
    movies_df = pd.read_parquet('movies_details.parquet')
except FileNotFoundError:
    st.error("The file 'movies_details.parquet' was not found. Please ensure the file is in the correct location.")
    movies_df = pd.DataFrame()  # Create an empty DataFrame to avoid further errors

# Ensure the DataFrame is not empty before proceeding
if not movies_df.empty:
    recommendations_tab(movies_df)