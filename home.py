# importing necessary libraries
import streamlit as st
from src.data_processing import load_df

# customizing the page
st.set_page_config(
    page_title="**recommendations**",
    page_icon=":guitar:",
    layout="wide", 
    initial_sidebar_state="expanded"
)

with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # describing the dashboard
        st.markdown("# <h1 style='text-align: center;'> :rainbow[SONG RECOMMENDATION SYSTEM]</h1>", unsafe_allow_html=True)
        st.write("")
        st.markdown("This recommendation system leverages **:green[Spotify's]** API to suggest songs or artists similar to your selection.")
        st.write("Using each song’s audio features as vectors, it applies *cosine similarity* to identify the closest matches.")
        st.write("Additionally, you can adjust the weights of different features to personalize your recommendations based on what matters most to you.")
        st.write("To help you explore these relationships, the app provides various visualizations that compare songs and artists in different ways.")
        st.write("Discover new music, fine-tune your recommendations, and enjoy the experience! :guitar:")
        st.markdown("### <h2 style='text-align: center;'>🎵🎵 ***:green[Enjoy!]*** 🎵🎵</h2>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""

            
""")
st.write("")
st.write("")
st.markdown("### :green[Features used in the recommendation system(description from Spotify's API):]")

# description of each feature

#add some colors to the description
colors = ['red', 'blue', 'green', 'violet', 'orange']

feature_descriptions = {
                            
    f"**:{colors[0]}[Danceability]**": "Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.",
    f"**:{colors[1]}[Energy]**": "Represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
    f"**:{colors[2]}[Acousticness]**": "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
    f"**:{colors[3]}[Instrumentalness]**": "Predicts whether a track contains no vocals. \"Ooh\" and \"aah\" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly \"vocal\". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
    f"**:{colors[4]}[Speechiness]**": "Detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.",
    f"**:{colors[0]}[Liveness]**": "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
    f"**:{colors[1]}[Valence]**": "Describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
    f"**:{colors[2]}[Tempo]**": "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
    f"**:{colors[3]}[Loudness]**": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.",
    f"**:{colors[4]}[Duration]**": "The duration of the track in minutes."
}


with st.container(height=300):
    for feature, description in feature_descriptions.items():

        with st.expander(feature):
            st.markdown(description)



st.markdown("""
      


""")
st.markdown("""
      


""")

st.write("")
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(' ***:green[Guillermo Contreras]***')
        st.write("Aspiring Data engineer | Machine Learning Engineer")
        st.write("Passionate about data, music, and technology.")   
        st.markdown("***Contact information:***")


        # contact info
        contact = {
        
            "LinkedIn": "https://www.linkedin.com/in/guillermocontp/",
            'Github repo': 'https://github.com/guillermocontp/recommendation-system'
                }

        cols = st.columns(2)

        # showing contact info 
        for (name, contact_info), col in zip(contact.items(), cols):
            with col:
                
                st.link_button(label=name, url=contact_info)
                st.write("")

#Initializing the variables from load_and_cache
if "data_loaded" not in st.session_state:  
    variables = load_df()  # Call the function once
    keys = ['tracks',"mapping", "artists",  "audio_features"]
    
    # Store all variables in session state dynamically
    for key, value in zip(keys, variables):
        st.session_state[key] = value
    
    st.session_state.data_loaded = True  # Flag to avoid reloading


