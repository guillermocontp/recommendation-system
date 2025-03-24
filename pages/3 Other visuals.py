import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.data_processing import (get_artist_features, 
                                 vectorize_artist_features,
                                 merge_artist_features,
                                 track_page_navigation,
                                 track_button_clicks)
import plotly.graph_objects as go
import pandas as pd


# Track page view
track_page_navigation("Other Visuals")  

# Track button clicks on this page
track_button_clicks()


# bring the necessary data
tracks = st.session_state.tracks
mapping = st.session_state.mapping
artists = st.session_state.artists
audio_features = st.session_state.audio_features

st.markdown("### <h1 style='text-align: center;'> :rainbow[Other visuals]</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("#### <h2 style='text-align: center;'>Artist Similarity Matrix</h2>", unsafe_allow_html=True)


# Check session state first
if 'artists' in st.session_state and 'audio_features' in st.session_state:
    # Get data from session state
    artists = st.session_state.artists
    
    audio_features = st.session_state.audio_features
    tracks_features = pd.merge(tracks, audio_features, on='track_id', how='inner')
    artist_track_ = merge_artist_features(tracks, mapping, artists)
    # Process data
    table_artists = get_artist_features(artists, artist_track_, audio_features)
    
    vectors_artists, _ = vectorize_artist_features(table_artists)
    
    # Get 5 random unique indices
    random_indices = np.random.choice(len(vectors_artists), size=5, replace=False)

    # Calculate similarity matrix for first 5 artists
    
    similarity_matrix = cosine_similarity(vectors_artists[random_indices])
    names = artists['name'].iloc[random_indices].tolist()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=similarity_matrix,
        x=names,
        y=names,
        hoverongaps=False,
        colorscale='Viridis',
        text=[[f'{val:.4f}' for val in row] for row in similarity_matrix],
        texttemplate='%{text}',
        textfont={"size": 12},
        showscale=True
    ))

    # Update layout
    fig.update_layout(
        title='Artist Similarity Matrix',
        xaxis_title='Artist',
        yaxis_title='Artist',
        width=700,
        height=700
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)


   