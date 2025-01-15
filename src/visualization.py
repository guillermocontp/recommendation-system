import plotly.express as px

def plot_yearly_features(df):
    """
    Plot yearly means of selected features.
    
    Args:
        df: pandas DataFrame containing the data
        features: list of feature columns to plot
        
    Returns:
        plotly figure object
    """    
    features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'valence']
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