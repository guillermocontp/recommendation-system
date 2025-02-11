import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


from src.data_processing import (merge_artist_features, 
                                 process_artist_data, 
                                 get_artist_features, 
                                 vectorize_artist_features, 
                                 apply_feature_weights, 
                                 get_artist_sample, 
                                 get_similar_artists
                                    )

from src.visualization import align_datasets, visualize_artist_space

from src.spotify_widget import (fetch_and_parse_spotify_artist_data, 
                                show_spotify_artist_components
                                )

from src.spotify_widget import (
    get_token
)

# bring the necessary data
tracks = st.session_state.tracks
mapping = st.session_state.mapping
artists = st.session_state.artists
audio_features = st.session_state.audio_features
artist_track_ = st.session_state.artist_track_

# loading Spotify credentials (for API) from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = get_token(client_id, client_secret)

# processing the data

table = get_artist_features(artists, artist_track_, audio_features)

vectors = vectorize_artist_features(table)

#we will not play with the werights for now
#weighted_vectors = apply_feature_weights(vectors)

#page layout


artist_list = sorted(artist_track_['name_x'].unique())

selected_artist = st.selectbox(
    "Search for an artist",
    options=artist_list,
    index=None,
    placeholder="Type artist name..."
)

st.header('Artist Profile')
st.markdown("---")
st.write("")

# error handling if no artist is selected
if selected_artist == None:
    st.write("Please select an artist")
else:
    artist_match = artist_track_[artist_track_['name_x'] == selected_artist]   
    artist_id = artist_match['artist_id']
    
    artist_id = artist_id.values[0]


    
# creating columns
col1, col2 = st.columns(2, gap="small" )
with col1:
    # fetching and visualizing the selected artist data
    test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)#I have to initialize variables
    show_spotify_artist_components(test_fetch) #this function displays in columns the info, this is coded into it REVISE


with col2:
    # fetching and visualizing the similar artists' profiles
    similar_artists = get_similar_artists(selected_artist, vectors, artists)
    if isinstance(similar_artists, str):
        artist_match = artist_track_[artist_track_['name_x'] == similar_artists]   
        artist_id = artist_match['artist_id']    
        artist_id = artist_id.values[0]
        test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)#I have to initialize variables
        show_spotify_artist_components(test_fetch) #this function displays in columns the info, this is coded into it REVISE

    else:
        for artist, score in similar_artists:
            artist_match = artist_track_[artist_track_['name_x'] == artist]   
            artist_id = artist_match['artist_id']    
            artist_id = artist_id.values[0]
            test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)#I have to initialize variables
            show_spotify_artist_components(test_fetch) #this function displays in columns the info, this is coded into it REVISE
            st.metric("Similarity Coeficient", f"{score:,}" )
            