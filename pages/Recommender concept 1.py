import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


from src.data_processing import (data_to_radar_chart, 
                                 process_artist_data, 
                                 get_artist_features, 
                                 vectorize_artist_features, 
                                 apply_feature_weights, 
                                 reset_weights_callback, 
                                 get_similar_artists
                                    )

from src.visualization import (create_radar_chart_new, 
                               visualize_artist_space
)

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

# Initialize variables for visualization
similar_vectors = None
similar_artists = None
scores = None


features = ['danceability', 'energy', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'speechiness', 'key', 'mode', 
                'tempo', 'time_signature']
    
weight_values = [0.1, 0.5, 1, 1.5, 2.0, 3.0, 5.0]
weights = {}

# processing the data
table = get_artist_features(artists, artist_track_, audio_features)

vectors, artists_cleaned = vectorize_artist_features(table)
# Store original vectors for reset
st.session_state.original_vectors = vectors.copy()



#page layout
#SIDEBAR: artist selection


with st.sidebar:
    artist_list = sorted(artist_track_['name_x'].unique())
    selected_artist = st.selectbox(
        "Search for an artist",
        options=artist_list,
        index=None,
        placeholder="Type artist name..."
    )

# Main page layout, two columns
main_col1, main_col2 = st.columns([1, 1])

# First main column: Feature weights
with main_col1:
    
    with st.container():
                
        # Add Reset button next to title
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Customize Feature Weights")
        with col2:
            if st.button("Reset Weights", use_container_width=True, on_click=reset_weights_callback):
                st.rerun()
        
        
        # Initialize or get weights from session state
        if 'weights' not in st.session_state:
            st.session_state.weights = {}
        
        weights = st.session_state.weights


        # Create scrollable container for feature weights
        with st.container(height=500):
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
            

with main_col2:
    # Second container: Artist selection    
    if selected_artist is None:
        st.write("Please select an artist")
    else:
        artist_match = artist_track_[artist_track_['name_x'] == selected_artist]   
        artist_id = artist_match['artist_id'].values[0]
        test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)
        st.image(test_fetch['artist_image'].iloc[0], use_container_width=True, width=50)
        st.write("") 
        # Display artist info
        st.subheader(test_fetch['artist_name'].iloc[0])
                        
        st.link_button('Go to Spotify profile', test_fetch['spotify_url'].iloc[0], use_container_width=True)
                    

st.markdown("---")

# Recommendations container
with st.container():
    st.subheader('Similar Artists')
    if selected_artist is not None:
        vectors_to_use = st.session_state.get('vectors', vectors)
        result = get_similar_artists(selected_artist, vectors_to_use, artists_cleaned)
        
        if isinstance(result, str):
            st.error(result)
            similar_vectors = None  # Reset if error
            similar_artists = None
            scores = None
        else:
            # Create three columns for recommendations
            similar_vectors, similar_artists, scores = result
            second_artist = similar_artists.iloc[1]['name']
            rec_cols = st.columns(3, gap="small")
            
             # Only loop through top 3 artists for display
            for idx in range(3):
                with rec_cols[idx]:
                    artist = similar_artists.iloc[idx+1]['name']
                    score = scores[idx+1]
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
                        st.metric("Similarity Score", f"{score:.4f}")


# Visualize artist space
with st.container():
    st.subheader("Visualize Artist Space")
    if similar_vectors is not None:
        fig = visualize_artist_space(similar_vectors, similar_artists, scores, item_type='artist')
        st.plotly_chart(fig,  use_container_width=True)
   

# visualize artist audio profile
with st.container():
    st.header('Artist Comparison')
    st.subheader('Radar chart comparison')
    st.markdown("---")
    
    # error handling if no artist is selected
    if selected_artist == None or second_artist == None:
        st.write("Please select an artist")
    else:
        artist1_mean = process_artist_data(selected_artist, artist_track_, audio_features)
        artist2_mean = process_artist_data(second_artist, artist_track_, audio_features)
    
        data_radar = data_to_radar_chart(artist1_mean, artist2_mean)
        fig = create_radar_chart_new(data_radar)
        st.plotly_chart(fig, use_container_width=True)