import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

def plot_yearly_features(df):
    """
    Plot yearly means of selected features.
    
    Args:
        df: pandas DataFrame containing the data
        features: list of feature columns to plot
        
    Returns:
        plotly figure object
    """    
    features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'speechiness']
    yearly_means = df.groupby('year')[features].mean().reset_index()
    
    fig = px.line(
        yearly_means,
        x='year',
        y=features,
    )
    
    # Set x-axis tick interval to 1 year
    fig.update_layout(
        xaxis=dict(dtick=1)
    )
    
    return fig

def plot_single_feature(df, selected_feature):
    """
    Plot yearly mean of a single selected feature.
    
    Args:
        df: pandas DataFrame containing the data
        selected_feature: string name of feature to plot
        
    Returns:
        plotly figure object
    """
    yearly_means = df.groupby('year')[selected_feature].mean().reset_index()
    
    fig = px.line(
        yearly_means,
        x='year',
        y=selected_feature,
    )
    
    fig.update_layout(
        xaxis=dict(dtick=1)
    )
    
    return fig

def plot_feature_averages(melted_audio_df):
    """
    Create bar plot of average feature values.
    
    Args:
        melted_audio_df: pandas DataFrame in melted format with Feature and Average Value columns
        
    Returns:
        plotly figure object
    """
    fig = px.bar(
        melted_audio_df,
        x='Feature',
        y='Average Value',
        template='plotly_white',
    )
    
    return fig

def plot_year_comparison(comparison_audio_df):
    """
    Create grouped bar chart comparing features between years.
    
    Args:
        comparison_audio_df: DataFrame containing Feature, Value and Year columns
    Returns:
        plotly figure object
    """
    fig = px.bar(
        comparison_audio_df,
        x='Feature',
        y='Value',
        color='Year',
        barmode='group',
        template='plotly_white',
        color_discrete_sequence=['#0068C9', '#C3E4FF']
    )
    
    return fig

def style_chart(fig):
    """
    Apply consistent styling to plotly charts.
    
    Args:
        fig: plotly figure object
    Returns:
        styled plotly figure object
    """
    fig.update_layout(
        height=600,
        showlegend=True,
        xaxis_title='',
        yaxis_title='Value',
        yaxis=dict(range=[0, 1], tickmode='linear', dtick=0.1),
        font=dict(color='#FFFFFF'),
    )
    return fig

def display_metrics(avg_filtered_track_df, avg_data):
    """
    Display metrics in three columns using Streamlit.
    """
    # Create columns
    m1, m2, m3 = st.columns(3)
    
    # Tempo metric
    with m1:
        tempo_delta = round(avg_filtered_track_df['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
        st.metric(
            label="Average Tempo",
            value=f"{round(avg_filtered_track_df['Tempo (BPM)'].mean())} BPM",
            delta=f"{tempo_delta} BPM"
        )
    
    # Loudness metric
    with m2:
        loudness_delta = round(avg_filtered_track_df['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
        st.metric(
            label="Average Loudness",
            value=f"{round(avg_filtered_track_df['Loudness (dB)'].mean())} dB",
            delta=f"{loudness_delta} dB"
        )
    
    # Duration metric
    with m3:
        duration_delta = round(avg_filtered_track_df['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
        st.metric(
            label="Average Duration",
            value=f"{round(avg_filtered_track_df['Duration (min)'].mean(), 2)} min",
            delta=f"{duration_delta} min"
        )
    
    return m1, m2, m3


def create_radar_chart(table):
    """
        Takes a table with several features and plots them into a radar chart
    """
    song_names = table['name']

    # Features to compare
    features = ['energy', 'danceability', 'acousticness', 'mode', 'valence']

    # Prepare labels and angles for the radar chart
    labels = features
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the circle

    # Create a radar chart for both songs
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for song_name in song_names:
        # Extract the feature values for the song
        values = table.loc[table['name'] == song_name, features].values.flatten()
        values = np.append(values, values[0])  # Close the radar chart

        # Plot the radar chart for the song
        ax.fill(angles, values, alpha=0.4, label=song_name)
        ax.plot(angles, values, linewidth=2)

    # Customization
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Set y-axis ticks
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_title('Feature Comparison of Songs', size=15, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))



    return fig

def create_radar_chart_new(table):
    """Creates radar chart comparing song features using Plotly."""
    
    features = ['energy', 'danceability', 'acousticness', 'mode', 'valence']
    song_names = table['name'].unique()

    fig = go.Figure()

    for song_name in song_names:
        values = table.loc[table['name'] == song_name, features].values.flatten()
        
        # Add trace for each song
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=features,
            fill='toself',
            name=song_name
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title={
            'text':'',  #'Feature Comparison of Songs',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        width=500,
        height=500
    )

    return fig


def clean_artist_name(name):
    """Clean artist name for plotting"""
    import re
    # Replace special characters with underscore
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '_', str(name))
    return cleaned

def align_datasets(vectors, artists_df):
        """ Align datasets for visualization """
        common_indices = vectors.index.intersection(artists_df.index)
        vectors_aligned = vectors.loc[common_indices]
        artists_aligned = artists_df.loc[common_indices]


            # Reset indices
        vectors_aligned = vectors_aligned.reset_index(drop=True)
        artists_aligned = artists_aligned.reset_index(drop=True)

        return vectors_aligned, artists_aligned


def visualize_artist_space(vectors, artists_df, weights=None):
    """
    Visualize artists in 2D space with optional feature weights
    """


    
    # Apply weights if provided
    if weights is None:
        weights = {col: 1.0 for col in vectors.columns}
    
    weighted_vectors = vectors.copy()
    for col, weight in weights.items():
        if col in weighted_vectors.columns:
            weighted_vectors[col] = weighted_vectors[col] * weight
    
    # Normalize and reduce dimensionality
    scaler = StandardScaler()
    vectors_scaled = scaler.fit_transform(weighted_vectors)
       # Set appropriate perplexity (should be smaller than n_samples)
    perplexity = min(30, len(vectors) - 1)
    tsne = TSNE(
        n_components=2, 
        random_state=42,
        perplexity=perplexity,
        n_iter=1000
    )
    vectors_2d = tsne.fit_transform(vectors_scaled)
    
    
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], alpha=0.6)
    
    # Add artist names as labels
    for i in range(len(vectors_2d)):
            plt.annotate(artists_df.iloc[i]['clean_name'], 
                        (vectors_2d[i, 0], vectors_2d[i, 1]),
                        xytext=(5, 5), 
                        textcoords='offset points',
                        fontsize=8)
    
    plt.title('Artist Similarity Space (2D Projection)')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    
    return plt