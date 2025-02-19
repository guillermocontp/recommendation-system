import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.data_processing import (get_artist_features, vectorize_artist_features)
import plotly.graph_objects as go
import pandas as pd



# bring the necessary data
tracks = st.session_state.tracks
mapping = st.session_state.mapping
artists = st.session_state.artists
audio_features = st.session_state.audio_features
artist_track_ = st.session_state.artist_track_


# Check session state first
if 'artists' in st.session_state and 'artist_track_' in st.session_state and 'audio_features' in st.session_state:
    # Get data from session state
    artists = st.session_state.artists
    artist_track_ = st.session_state.artist_track_
    audio_features = st.session_state.audio_features
    tracks_features = pd.merge(tracks, audio_features, on='track_id', how='inner')
    # Process data
    table_artists = get_artist_features(artists, artist_track_, audio_features)
    vector_songs= vectorize_artist_features(tracks_features)
    vectors_artists = vectorize_artist_features(table_artists)
    
    # Calculate similarity matrix for first 5 artists
    n_items = 5
    similarity_matrix = cosine_similarity(vectors_artists[:n_items])
    names = artists['name'].iloc[:n_items].tolist()
    
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


    # Calculate similarity matrix for first 5 artists
    n_items1 = 5
    similarity_matrix2 = cosine_similarity(vector_songs[:n_items1])
    names = tracks['name'].iloc[:n_items1].tolist()
    
    # Create heatmap
    fig2 = go.Figure(data=go.Heatmap(
        z=similarity_matrix2,
        x=names,
        y=names,
        hoverongaps=False,
        colorscale='Viridis',
        text=[[f'{val:.4f}' for val in row] for row in similarity_matrix2],
        texttemplate='%{text}',
        textfont={"size": 12},
        showscale=True
    ))

    # Update layout
    fig2.update_layout(
        title='Artist Similarity Matrix',
        xaxis_title='Song',
        yaxis_title='Song',
        width=700,
        height=700
    )

    # Display the plot
    st.plotly_chart(fig2, use_container_width=True)