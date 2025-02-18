import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import pandas as pd
import random





def create_radar_chart_new(table):
    """Creates radar chart comparing song features using Plotly.
    """
    features = ['energy', 'danceability', 'acousticness', 'mode', 'valence', 'energy']
    song_names = table['name'].unique()

    # Define vibrant colors with different transparencies for line and fill
    colors = [
        {'line': 'rgba(255, 65, 54, 1)',   'fill': 'rgba(255, 65, 54, 0.2)'},     # red
        {'line': 'rgba(86, 215, 198, 1)',  'fill': 'rgba(86, 215, 198, 0.2)'},    # turquoise
        {'line': 'rgba(255, 171, 0, 1)',   'fill': 'rgba(255, 171, 0, 0.2)'},     # yellow
        {'line': 'rgba(153, 102, 255, 1)', 'fill': 'rgba(153, 102, 255, 0.2)'},   # purple
        {'line': 'rgba(0, 204, 150, 1)',   'fill': 'rgba(0, 204, 150, 0.2)'}      # green
    ]

    # Randomly shuffle the colors
    random_colors = random.sample(colors, len(song_names))
    fig = go.Figure()

    for idx, song_name in enumerate(song_names):
        values = table.loc[table['name'] == song_name, features].values.flatten()
        color = random_colors[idx]
        # Add trace for each song with custom colors
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=features,
            fill='toself',
            name=song_name,
            line=dict(color=color['line'], width=2),
            fillcolor=color['fill']
        ))

    # Update layout with transparent background
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor="rgba(255, 255, 255, 0.2)",
                linecolor="rgba(255, 255, 255, 0.2)"
            ),
            angularaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.2)",
                linecolor="rgba(255, 255, 255, 0.2)"
            ),
            bgcolor="rgba(0, 0, 0, 0)"
        ),
        showlegend=True,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        width=500,
        height=500,
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.2
        )
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


def visualize_artist_space(vectors, items_df, scores=None, item_type="artist"):
    """
    Visualize artists in 2D space with optional feature weights
    """

        # Apply StandardScaler before t-SNE
    scaler = StandardScaler()
    vectors_scaled = scaler.fit_transform(vectors)

    perplexity = min(30, len(vectors) - 1)
    tsne = TSNE(
        n_components=2, 
        random_state=42,
        perplexity=perplexity,
        max_iter=1000
    )
    vectors_2d = tsne.fit_transform(vectors_scaled)

        # Use dictionary for dynamic labels
    labels = {
        "artist": {
            "title": "Artist Similarity Space",
            "hover": "Artist: %{customdata[0]}",
            "types": ["Selected Artist", "Top 3 Similar", "Similar Artist"],
            "hover_template": ["Artist: %{customdata[0]}", "Similarity: %{customdata[1]:.3f}"],
            "color_map": {
                "Selected Artist": "#ff0000",
                "Top 3 Similar": "#00ff00",
                "Similar Artist": "#636efa"
            },
            "hover_data": {
                "Artist": True,
                "Similarity": ":.3f",
                "x": False,
                "y": False,
                "Size": False
            },
            "default_type": "Similar Artist",
            "selected_type": "Selected Artist",
            "top3_type": "Top 3 Similar"
        },
        "song": {
            "title": "Song Similarity Space",
            "hover": "Song: %{customdata[0]}",
            "types": ["Selected Song", "Top 3 Similar", "Similar Song"],
            "hover_template": ["Song: %{customdata[0]}", "Similarity: %{customdata[1]:.3f}"],
            "color_map": {
                "Selected Song": "#ff0000",
                "Top 3 Similar": "#00ff00",
                "Similar Song": "#636efa"
            },
            "hover_data": {
                "Song": True,
                "Similarity": ":.3f",
                "x": False,
                "y": False,
                "Size": False
            },
            "default_type": "Similar Song",
            "selected_type": "Selected Song",
            "top3_type": "Top 3 Similar"
        }
    }[item_type]


     # Create DataFrame using dynamic labels
    plot_df = pd.DataFrame({
        'x': vectors_2d[:, 0],
        'y': vectors_2d[:, 1],
        'Item': items_df['name'],        
        'Similarity': [1.0 if i == 0 else float(scores[i]) for i in range(len(vectors_2d))]
    })

   

    # Assign types based on original similarity scores
    plot_df['Type'] = labels["default_type"]  # default type
    
    plot_df.iloc[0, plot_df.columns.get_loc('Type')] = labels["selected_type"]
    

    # Find indices of top 3 similar artists (excluding selected artist)
    top3_indices = scores[1:].argsort()[-3:][::-1] + 1  # add 1 to skip selected artist
    plot_df.iloc[top3_indices, plot_df.columns.get_loc('Type')] = labels["top3_type"]    
    
    # Size based on similarity but larger for selected and top 3
    plot_df['Size'] = plot_df.apply(lambda x: 
        50 if x['Type'] == labels["selected_type"]
        else 40 if x['Type'] == labels["top3_type"]  
        else max(20, 30 * x['Similarity']), axis=1)
    
    
    # Create Plotly figure
    fig = px.scatter(
        plot_df,
        x='x',
        y='y',
        color='Type',
        size='Size',
        hover_data={
        'Item': True,
        'Similarity': ':.3f',
        'x': False,
        'y': False,
        'Size': False
    },
        color_discrete_map=labels["color_map"]
    )
    
    # Update layout
    fig.update_traces(
        textposition='top center',  # Remove text labels
        hovertemplate="<br>".join([
        f"{item_type.capitalize()}: %{{customdata[0]}}",
        "Similarity: %{customdata[1]:.3f}",
        "<extra></extra>"
    ])

    )
    
    fig.update_layout(
        title=labels["title"],
        xaxis_title='t-SNE 1',
        yaxis_title='t-SNE 2',
        showlegend=True,
        legend=dict(
            yanchor="auto",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    return fig