import streamlit as st
import pandas as pd
from .display import recommendations_tab

# Load the Parquet file
movies_df = pd.read_parquet('movies_details.parquet')
