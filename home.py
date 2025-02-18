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
st.write("This is a recommendation system that uses Spotify API data to give you songs or artists that are similar than your pick.")
st.write("Using the features of the songs, I used them as vectors and I use cosine similarity for the pick.")
st.write("There is also the possibility to change the weights of the features to get a more personalized recommendation.")
st.write("The features are described below")
st.write("There are different visualizations of the songs/artists vectors, for comparison.")
st.write("Enjoy! :guitar:")

st.markdown("""

            
""")
st.write("")
st.write("")
# description of each feature
feature_descriptions = {
    "Danceability": "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.",
    "Energy": "Energy represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
    "Acousticness": "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
    "Instrumentalness": 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.',
    "Speechiness": "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
    "Liveness": "Liveness detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
    "Valence": "A describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
    "Tempo": "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
    "Loudness": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.",
    "Duration": "The duration of the track in minutes."
}

with st.container(height=300):
    for feature, description in feature_descriptions.items():

        with st.expander(feature):
            st.write(description)
st.markdown("""

            
""")
st.write("")
st.subheader('Created by Guillermo Contreras')


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
        st.link_button(':song:', contact_info)
        st.write("")

#Initializing the variables from load_and_cache
if "data_loaded" not in st.session_state:  
    variables = load_df()  # Call the function once
    keys = ['tracks_features','tracks',"mapping", "artists", "artist_track_", "audio_features"]
    
    # Store all variables in session state dynamically
    for key, value in zip(keys, variables):
        st.session_state[key] = value

    st.session_state.data_loaded = True  # Flag to avoid reloading


