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
features = ['danceability', 'energy', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'speechiness', 'key', 'mode', 
                'tempo', 'time_signature']
    
weight_values = [0.1, 0.5, 1, 1.5, 2.0, 3.0, 5.0]
weights = {}

table = get_artist_features(artists, artist_track_, audio_features)

vectors = vectorize_artist_features(table)


# Initialize selected_artist in session state if not present
#if 'selected_artist' not in st.session_state:
#    st.session_state.selected_artist = None

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
            current_artist = st.session_state.selected_artist
            # Reset vectors and weights
            st.session_state.vectors = vectors  # Reset to original vectors
            st.session_state.weights = {}  # Clear weights
            
            # Clear individual weight states
            for feature in features:
                if f"weight_{feature}" in st.session_state:
                    del st.session_state[f"weight_{feature}"]
            # Put artist back into session state
            st.session_state.selected_artist = current_artist
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
    col_search, col_artist = st.columns([1, 2], gap="small")
    
    with col_search:
        artist_list = sorted(artist_track_['name_x'].unique())
        selected_artist = st.selectbox(
            "Search for an artist",
            options=artist_list,
            index=None,
            placeholder="Type artist name...",
            key="selected_artist"
        )

    with col_artist:
        if selected_artist is None:
            st.write("Please select an artist")
        else:
            artist_match = artist_track_[artist_track_['name_x'] == selected_artist]   
            artist_id = artist_match['artist_id'].values[0]
            test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)
            show_spotify_artist_components(test_fetch)

st.markdown("---")

# Recommendations container
with st.container():
    st.subheader('Similar Artists')
    if selected_artist is not None:
        vectors_to_use = st.session_state.get('vectors', vectors)
        similar_artists = get_similar_artists(selected_artist, vectors_to_use, artists)
        
        if isinstance(similar_artists, str):
            st.write(similar_artists)
        else:
            # Create three columns for recommendations
            rec_cols = st.columns(3, gap="small")
            
            for idx, (artist, score) in enumerate(similar_artists):
                with rec_cols[idx]:
                    artist_match = artist_track_[artist_track_['name_x'] == artist]   
                    artist_id = artist_match['artist_id'].values[0]
                    test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)
                    # Display artist information
                    st.image(test_fetch['artist_image'].iloc[0], use_container_width=True, width=50)
                    st.write("") 
                    
                    # Display artist info
                    st.subheader(test_fetch['artist_name'].iloc[0])
                   
                    # Display metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button('Go to Spotify profile', test_fetch['spotify_url'].iloc[0], use_container_width=True)
                    with col2:
                        st.metric("Similarity Score", f"{score:.3f}")
                    

            