import streamlit as st

# Import the modules using relative imports
from individual_movies import movie_data
from recommendations import movie_recs

# Create tabs
tab1, tab2 = st.tabs(["Movie Data", "Recommendations"])

with tab1:
    movie_data.movie_info_tab()

with tab2:
    movie_recs.recommendations_tab()
