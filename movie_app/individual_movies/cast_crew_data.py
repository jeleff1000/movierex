import streamlit as st
import pandas as pd

# Define the relative path to the Parquet file
parquet_file_path = 'individual_movies/people_details.parquet'

# Load the Parquet file
df = pd.read_parquet(parquet_file_path)

def display_people_details():
    """Display key details of people."""
    st.title('Cast and Crew Details')

    # Get query parameters
    query_params = st.query_params
    selected_person = query_params.get("person", "")

    # Dropdown with all people names
    all_people_names = [""] + sorted(df['name'].tolist())
    selected_person = st.selectbox("", all_people_names, index=all_people_names.index(selected_person) if selected_person in all_people_names else 0)

    # Update query parameters when a person is selected
    if selected_person:
        st.query_params.person = selected_person

    # Display selected person details
    if selected_person:
        person_details = df[df['name'] == selected_person].iloc[0]

        # Create columns for image and details
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(person_details['images'].split(', ')[0], width=200)

        with col2:
            st.markdown(f"**Name:** {person_details['name']}")
            st.markdown(f"**Biography:** {person_details['biography']}")
            st.markdown(f"**Birthday:** {person_details['birthday']}")
            st.markdown(f"**Deathday:** {person_details['deathday']}")
            st.markdown(f"**Known For:** {person_details['known_for_department']}")
            st.markdown(f"**Place of Birth:** {person_details['place_of_birth']}")

        # Display movie credits with expand option
        movie_credits = person_details['movie_credits'].split(', ')
        st.markdown("**Movie Credits:**")
        st.markdown(", ".join(movie_credits[:5]))
        if len(movie_credits) > 5:
            with st.expander("Show more movie credits"):
                st.markdown(", ".join(movie_credits[5:]))

        # Display TV credits with expand option
        tv_credits = person_details['tv_credits'].split(', ')
        st.markdown("**TV Credits:**")
        st.markdown(", ".join(tv_credits[:5]))
        if len(tv_credits) > 5:
            with st.expander("Show more TV credits"):
                st.markdown(", ".join(tv_credits[5:]))

# Ensure this function call is placed correctly within your Streamlit script
if __name__ == "__main__":
    display_people_details()