import streamlit as st

def create_person_buttons(names, people_df):
    """Create buttons for names that exist in the people_details database."""
    names_list = names.split(', ')
    buttons = []
    for i in range(0, len(names_list), 4):
        cols = st.columns(4)
        for col, name in zip(cols, names_list[i:i+4]):
            if name in people_df['name'].values:
                if col.button(name, key=f"person_{name}"):
                    st.query_params.update({'person': name, 'scrollTo': 'cast-and-crew-details'})
                    st.rerun()
            else:
                col.write(name)
            buttons.append(name)
    return ' '.join(buttons)