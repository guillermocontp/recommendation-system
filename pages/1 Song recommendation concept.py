import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from src.data_processing import (data_to_radar_chart, 
                                 process_songs, 
                                    reset_weights_callback,
                                 vectorize_artist_features, 
                                 apply_feature_weights, 
                                 get_similar_artists,
                                   )

from src.visualization import create_radar_chart_new, visualize_artist_space

from src.spotify_widget import (
                                fetch_and_parse_spotify_songs,
                                get_token
                                )



# bring the necessary data
tracks = st.session_state.tracks
audio_features = st.session_state.audio_features
tracks_features = pd.merge(tracks, audio_features, on='track_id', how='inner')

# loading Spotify credentials (for API) from .env file
client_id = st.secrets["spotify"]["client_id"]
client_secret = st.secrets["spotify"]["client_secret"]
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

vectors, songs_cleaned = vectorize_artist_features(tracks_features)
st.session_state.original_vectors = vectors.copy()



#page layout
#SIDEBAR: artist selection


with st.sidebar:

# First container: Feature weights
    

        song_list = sorted(tracks_features['name'].unique())
        selected_song = st.selectbox(
            "Search for a song",
            options=song_list,
            index=None,
            placeholder="Type song name..."
        )
with st.container(border=True):
        st.markdown('### :rainbow[Song recommendations]')
        
        st.write(" ")  
        if st.session_state.get("ab_variant", "A") == "A":
            st.markdown("""
                        * Select a song from the list. The system will recommend three similar songs based on audio features.
                        * Adjust feature weights to customize the recommendations—prioritize certain aspects like danceability, energy, or tempo.
                            * With the feature weighting option, you can adjust the importance of each attribute (e.g., giving more weight to danceability or tempo) to refine the recommendations.
                        * Explore visualizations below to compare the selected song and recommendations in different ways, including radar charts and t-SNE projections.
                        """)
        else:
            st.markdown("""
                        * Select a song from the list
                        * Adjust feature weights
                        * Explore visualizations below  
                            """)              

# Main page layout, two columns
main_col1, main_col2 = st.columns([1, 1])


# First main column: Feature weights
with main_col1:
    with st.container():
    # Add Reset button next to title
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('### :rainbow[Customize Feature Weights]')
            
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
                st.session_state.song_vectors = vectors_weighted
            

# Second main col: Artist selection
with main_col2:      

    
    if selected_song is None:
        st.write("Please select a song")
    else:
        song_match = tracks_features[tracks_features['name'] == selected_song]   
        song_id = song_match['track_id'].values[0]
        test_fetch = fetch_and_parse_spotify_songs(song_id, token, client_id, client_secret)
        song_name = test_fetch['song_name'].iloc[0]
       # Create two columns for title and button
        title_col, button_col = st.columns([2, 1])
        with title_col:
            st.markdown(f'#### :rainbow[Selected song: {song_name}]')
        with button_col:
            st.link_button('Go to Spotify profile', 
                        test_fetch['spotify_url'].iloc[0], 
                        use_container_width=True)
        
        # Image below the columns
        st.image(test_fetch['cover_image'].iloc[0], use_container_width=True)
        st.write("")

st.markdown("---")

# Recommendations container
with st.container():
    st.markdown('#### :rainbow[Similar songs]')
    if selected_song is not None:
        vectors_to_use = st.session_state.get('song_vectors', vectors)
        result = get_similar_artists(selected_song, vectors_to_use, songs_cleaned)
        
        if isinstance(result, str):
            st.error(result)
            similar_vectors = None  # Reset if error
            similar_songs = None
            scores = None
        else:
            similar_vectors, similar_songs, scores = result
            #store top1 similar song for radar chart
            top1_song = similar_songs.iloc[1]['name']

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
                    
                    st.image(test_fetch['cover_image'].values[0], use_container_width=True, width=150)
                    st.markdown(f"**{test_fetch['song_name'].values[0]}**<br>{test_fetch['artist_name'].values[0]}", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button('Listen on Spotify', test_fetch['spotify_url'].values[0])
                    with col2:
                        st.metric("Similarity Score", f"{score:.4f}")
                    
                    st.write("") 

st.markdown("---")
st.markdown("""
            """)

# Visualize song space
with st.container():
    st.markdown('#### :rainbow[t-SNE Visualization: Understanding Song Similarity in 2D]')
    st.markdown("""
                * t-SNE reduces high-dimensional data into 2D while preserving local similarities, making it easier to spot clusters of similar songs. However, global distances may be distorted.
                * Cosine similarity directly measures vector similarity in high dimensions, but it’s harder to visualize. A song may have high cosine similarity to another but appear distant in t-SNE due to how the reduction prioritizes local structure.
                """)
    
    if similar_vectors is not None:
        fig = visualize_artist_space(similar_vectors, similar_songs, scores,item_type='song')
        st.plotly_chart(fig,  use_container_width=True)
st.markdown("---")
st.markdown("""
            """)

# visualize artist audio profile
with st.container():
    
    st.markdown('#### :rainbow[Radar chart comparison]')
    st.markdown("""
                * Compare the audio features of the selected song with the most similar song.
                * A radar chart compares two songs across multiple features, showing how their individual attributes align. If their shapes are similar, the songs share similar characteristics.
                * Cosine similarity directly measures vector similarity in high dimensions, but it’s harder to visualize. A song may have high cosine similarity to another but appear distant in t-SNE due to how the reduction prioritizes local structure.
                """)
    
   
    
    # error handling if no artist is selected
    if selected_song == None or top1_song == None:
        st.write("Please select an artist")
    else:
        song1 = process_songs(selected_song, tracks_features)
        song2 = process_songs(top1_song, tracks_features)
        data_radar = data_to_radar_chart(song1, song2)
        fig = create_radar_chart_new(data_radar)
        st.plotly_chart(fig, use_container_width=True)