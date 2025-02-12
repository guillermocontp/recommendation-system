import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import pandas as pd

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







def create_radar_chart_new(table):
   """Creates radar chart comparing song features using Plotly.
   """
   features = ['energy', 'danceability', 'acousticness', 'mode', 'valence']
   song_names = table['name'].unique()

    # Define vibrant colors
   colors = ['rgba(255, 65, 54, 0.7)',    # red
                'rgba(86, 215, 198, 0.7)',    # turquoise
                'rgba(255, 171, 0, 0.7)',     # yellow
                'rgba(153, 102, 255, 0.7)',   # purple
                'rgba(0, 204, 150, 0.7)']     # green

   fig = go.Figure()

   for idx, song_name in enumerate(song_names):
        values = table.loc[table['name'] == song_name, features].values.flatten()
        
        # Add trace for each song with custom colors
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=features,
            fill='toself',
            name=song_name,
            line=dict(color=colors[idx % len(colors)]),
            fillcolor=colors[idx % len(colors)]
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


def visualize_artist_space(vectors, artists_df, scores=None):
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
    
    # Create DataFrame for Plotly with size based on similarity
    plot_df = pd.DataFrame({
        'x': vectors_2d[:, 0],
        'y': vectors_2d[:, 1],
        'Artist': artists_df['name'],        
        'Similarity': [1.0 if i == 0 else float(scores[i]) for i in range(len(vectors_2d))]
        
    })

    # Assign types based on original similarity scores
    plot_df['Type'] = 'Similar Artist'  # default type
    plot_df.iloc[0, plot_df.columns.get_loc('Type')] = 'Selected Artist'  # selected artist
    
    # Find indices of top 3 similar artists (excluding selected artist)
    top3_indices = scores[1:].argsort()[-3:][::-1] + 1  # add 1 to skip selected artist
    plot_df.iloc[top3_indices, plot_df.columns.get_loc('Type')] = 'Top 3 Similar'
    
    # Size based on similarity but larger for selected and top 3
    plot_df['Size'] = plot_df.apply(lambda x: 
        50 if x['Type'] == 'Selected Artist'
        else 40 if x['Type'] == 'Top 3 Similar'
        else max(20, 30 * x['Similarity']), axis=1)
    
    
    # Create Plotly figure
    fig = px.scatter(
        plot_df,
        x='x',
        y='y',
        color='Type',
        size='Size',
        hover_data={
            'Artist': True,
            'Similarity': ':.3f',
            'x': False,
            'y': False,
            'Size': False
        },
        color_discrete_map={
            'Selected Artist': '#ff0000',
            'Top 3 Similar': '#00ff00',
            'Similar Artist': '#636efa'
        }
    )
    
    # Update layout
    fig.update_traces(
        textposition='top center',  # Remove text labels
        hovertemplate="<br>".join([
            "Artist: %{customdata[0]}",
            "Similarity: %{customdata[1]:.3f}",
            "<extra></extra>"
        ])
    )
    
    fig.update_layout(
        title='Artist Similarity Space',
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