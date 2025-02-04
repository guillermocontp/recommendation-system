import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data_processing import merge_artist_features, process_artist_data, get_artist_features, vectorize_artist_features, apply_feature_weights, get_artist_sample
from src.visualization import clean_artist_name, align_datasets, visualize_artist_space

# bring the necessary data
tracks = st.session_state.variables['tracks']
mapping = st.session_state.variables['mapping']
artists = st.session_state.variables['artists']
audio_features = st.session_state.variables['audio_features']


# prepare the data
artist_features_ = merge_artist_features(tracks, mapping, artists)

table = get_artist_features(artist_features_, audio_features)

vectors = vectorize_artist_features(table)

weighted_veectors = apply_feature_weights(vectors)


similar_artists = get_similar_artists("LeAnn Rimes", weighted_vectors, artists)
if isinstance(similar_artists, str):
    print(similar_artists)
else:
    for artist, score in similar_artists:
        print(f"{artist}: {score:.3f}")



#visualize a sample of artists

vectors_sample, artists_sample1 = get_artist_sample(vectors, artists, 30)

vectors_aligned, artists_aligned = align_datasets(vectors_sample, artists_sample1)

# Example usage with different weights
weights_1 = {
    'danceability': 3,
    'energy': 0.5,
    'valence': 1.0
}

weights_2 = {
    'danceability': 0.5,
    'energy': 1,
    'valence': 3.0
}


# Plot with different weights
visualize_artist_space(vectors_aligned, artists_sample1, weights_1)
plt.title('Emphasis on Danceability')

visualize_artist_space(vectors_aligned, artists_sample1, weights_2)
plt.title('Emphasis on Energy')
plt.tight_layout()
plt.show()