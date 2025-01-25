import streamlit as st
import pandas as pd
import docx
import difflib

def upload_file(movie_options):
    """Upload a file and return its content as a list of movie titles."""
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "xlsx", "docx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode("utf-8").splitlines()
        elif uploaded_file.name.endswith('.csv'):
            content = pd.read_csv(uploaded_file, header=None).iloc[:, 0].tolist()
        elif uploaded_file.name.endswith('.xlsx'):
            content = pd.read_excel(uploaded_file, header=None).iloc[:, 0].tolist()
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            content = [para.text for para in doc.paragraphs if para.text]
        else:
            st.error("Unsupported file format")
            return []

        # Split content by line breaks and find closest matches
        closest_matches = []
        for line in content:
            titles = line.split('\n')
            for title in titles:
                match = difflib.get_close_matches(title, movie_options.keys(), n=1, cutoff=0.6)
                if match:
                    closest_matches.append(match[0])
        return closest_matches
    return []