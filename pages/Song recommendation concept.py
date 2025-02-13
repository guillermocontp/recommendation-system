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
                                show_spotify_artist_components,
                                fetch_and_parse_spotify_songs,
                                )

from src.spotify_widget import (
    get_token
)

# bring the necessary data
tracks = st.session_state.tracks
audio_features = st.session_state.audio_features
tracks_features = pd.merge(tracks, audio_features, on='track_id', how='inner')

# loading Spotify credentials (for API) from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = get_token(client_id, client_secret)

# Initialize variables for visualization
similar_vectors = None
similar_songs = None
scores = None
features = ['danceability', 'energy', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'speechiness', 'key', 'mode', 
                'tempo', 'time_signature']
    
weight_values = [0.1, 0.5, 1, 1.5, 2.0, 3.0, 5.0]
weights = {}

# processing the data

vectors = vectorize_artist_features(tracks_features)


#page layout

# First container: Feature weights
with st.container():
        # Define features and their possible weight values
    


    # Add Reset button next to title
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Customize Feature Weights")
    with col2:
        if st.button("Reset Weights", use_container_width=True):
            # Store current artist selection
            current_song = st.session_state.selected_song
            # Reset vectors and weights
            st.session_state.vectors = vectors  # Reset to original vectors
            st.session_state.weights = {}  # Clear weights
            
            # Clear individual weight states
            for feature in features:
                if f"weight_{feature}" in st.session_state:
                    del st.session_state[f"weight_{feature}"]
            # Put artist back into session state
            st.session_state.selected_song = current_song
            st.rerun()
    
    
    # Initialize or get weights from session state
    if 'weights' not in st.session_state:
        st.session_state.weights = {}
    
    weights = st.session_state.weights


    # Create scrollable container for feature weights
    with st.container(height=300):
        for feature in features:
            # Create two columns for each feature
            feat_col, slider_col = st.columns([1, 3])
            with feat_col:
                st.write(f"{feature.capitalize()}")
            with slider_col:
                weight = st.select_slider(
                    label=" ",  # empty label since we show feature name separately
                    options=weight_values,
                    value=st.session_state.get(f"weight_{feature}", weight_values[2]),  # Default to 1.5
                    key=f"weight_{feature}",
                    label_visibility="collapsed"  # Hide label completely
                )
                if weight != weight_values[2]:
                    weights[feature] = weight
                elif feature in weights:
                    del weights[feature]

    # Store weights in session state
    st.session_state.weights = weights       
    
    # Apply weights button
    if weights:
        if st.button("Apply Weights", use_container_width=True):
            vectors_weighted = apply_feature_weights(vectors, weights)
            st.session_state.vectors = vectors_weighted
            

# Second container: Artist selection

with st.container():
    col_search, col_song = st.columns([1, 2], gap="small")
    
    with col_search:
        song_list = sorted(tracks_features['name'].unique())
        selected_song = st.selectbox(
            "Search for a song",
            options=song_list,
            index=None,
            placeholder="Type song name...",
            key="selected_song"
        )

    with col_song:
        if selected_song is None:
            st.write("Please select an song")
        else:
            song_match = tracks_features[tracks_features['name'] == selected_song]   
            song_id = song_match['track_id'].values[0]
            test_fetch = fetch_and_parse_spotify_songs(song_id, token, client_id, client_secret)
            st.image(test_fetch['cover_image'].values[0], use_column_width=False, width=150)
            st.markdown(f"**{test_fetch['song_name'].values[0]}**<br>{test_fetch['artist_name'].values[0]}", unsafe_allow_html=True)
            st.link_button('Listen on Spotify', test_fetch['spotify_url'].values[0])
            st.write("") 

st.markdown("---")

# Recommendations container
with st.container():
    st.subheader('Similar Songs')
    if selected_song is not None:
        vectors_to_use = st.session_state.get('vectors', vectors)
        result = get_similar_artists(selected_song, vectors_to_use, tracks)
        
        if isinstance(result, str):
            st.error(result)
            similar_vectors = None  # Reset if error
            similar_songs = None
            scores = None
        else:
            similar_vectors, similar_songs, scores = result

            # Create three columns for recommendations
            
            rec_cols = st.columns(3, gap="small")
            
             # Only loop through top 3 artists for display
            for idx in range(3):
                with rec_cols[idx]:
                    artist = similar_songs.iloc[idx+1]['name']
                    score = scores[idx+1]
                    song_match = tracks_features[tracks_features['name'] == artist]   
                    track_id = song_match['track_id'].values[0]
                    test_fetch = fetch_and_parse_spotify_songs(track_id, token, client_id, client_secret)
                    # Display artist information
                    
                    st.image(test_fetch['cover_image'].values[0], use_column_width=False, width=150)
                    st.markdown(f"**{test_fetch['song_name'].values[0]}**<br>{test_fetch['artist_name'].values[0]}", unsafe_allow_html=True)
                    st.link_button('Listen on Spotify', test_fetch['spotify_url'].values[0])
                    st.write("") 

# Visualize artist space
with st.container():
    st.subheader("Visualize Artist Space")
    if similar_vectors is not None:
        fig = visualize_artist_space(similar_vectors, similar_songs, scores,item_type='song')
        st.plotly_chart(fig,  use_container_width=True)