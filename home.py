# importing necessary libraries
import streamlit as st
from src.data_processing import load_df

# customizing the page
st.set_page_config(
    page_title="created by Guillermo Contreras",
    page_icon=":guitar:",
    layout="wide", 
    initial_sidebar_state="expanded"
)


# describing the dashboard
st.header('SONG RECOMMENDATION SYSTEM')
st.markdown("---")
st.write("")

st.markdown("""

            
""")
st.write("")
st.write("")
st.write("")
st.header('Contact Information')
st.markdown("---")

# contact info
contact = {
   
    "LinkedIn": "https://www.linkedin.com/in/guillermocontp/",
    'Github repo': 'https://github.com/guillermocontp/recommendation-system'
          }

cols = st.columns(5)

# showing contact info 
for (name, contact_info), col in zip(contact.items(), cols):
    with col:
        st.markdown(f"**{name}**")
        st.link_button('Go to linkedin profile', contact_info)
        st.write("")

#Initializing the variables from load_and_cache
if "data_loaded" not in st.session_state:  
    variables = load_df()  # Call the function once
    keys = ['tracks_features','tracks',"mapping", "artists", "artist_track_", "audio_features"]
    
    # Store all variables in session state dynamically
    for key, value in zip(keys, variables):
        st.session_state[key] = value

    st.session_state.data_loaded = True  # Flag to avoid reloading


