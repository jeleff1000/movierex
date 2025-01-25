import streamlit as st
import pandas as pd
from .display import recommendations_tab

def load_recommendations_tab(movies_df):
    """Load the recommendations tab with the given DataFrame."""
    if not movies_df.empty:
        recommendations_tab(movies_df)
    else:
        st.error("The movies DataFrame is empty. Please ensure the data is loaded correctly.")