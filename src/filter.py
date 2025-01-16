import pandas as pd 
import streamlit as st

def create_sidebar_filters(audio_df):
    """
    Create sidebar filters for year range and feature view selection.
    
    Args:
        audio_df: DataFrame containing year data
        
    Returns:
        tuple: (start_year, end_year, feature_view)
    """
    # Get available years
    available_years = sorted(audio_df['year'].unique().tolist())
    
    # Create year range selectors
    start_year = st.sidebar.selectbox(
        "Start Year",
        options=available_years,
        index=0, 
        key='start_year'
    )

    end_year = st.sidebar.selectbox(
        "End Year",
        options=available_years,
        index=len(available_years)-1,
        key='end_year'
    )
    
    # Create feature view selector
    feature_view = st.sidebar.selectbox(
        'Select View',
        ['All characteristics', 'Single Characteristic'],
        key='feature_view'
    )
    
    return start_year, end_year, feature_view


def initialize_features_and_averages(track_df):
    """
    Initialize feature list and calculate average track data.
    
    Args:
        track_df: DataFrame with track features
        
    Returns:
        tuple: (features list, average data)
    """
    # Define features for visualization
    features = [
        'danceability',
        'energy',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence'
    ]
    
    # Calculate average data
    avg_data = track_df.mean()
    
    return features, avg_data


def filter_data_by_years(audio_df, track_df, start_year, end_year):
    """
    Filter audio and track dataframes by year range and calculate track averages.
    
    Args:
        audio_df: DataFrame with audio features
        track_df: DataFrame with track features
        start_year: int, starting year for filter
        end_year: int, ending year for filter
    
    Returns:
        tuple: (filtered_audio_df, filtered_track_df, avg_filtered_track_df)
    """
    filtered_audio_df = audio_df[(audio_df['year'] >= start_year) & (audio_df['year'] <= end_year)]
    filtered_track_df = track_df[(track_df['year'] >= start_year) & (track_df['year'] <= end_year)]
    avg_filtered_track_df = filtered_track_df.mean()
    
    return filtered_audio_df, filtered_track_df, avg_filtered_track_df

def prepare_yearly_feature_data(audio_df, year, features):
    """
    Filter data for specific year and prepare for visualization.
    
    Args:
        audio_df: DataFrame with audio features
        year: int, year to filter for
        features: list of feature columns
    
    Returns:
        DataFrame with Feature and Average Value columns
    """
    filtered_audio_df = audio_df[audio_df['year'] == year]
    melted_audio_df = filtered_audio_df[features].mean().reset_index()
    melted_audio_df.columns = ['Feature', 'Average Value']
    
    return melted_audio_df

def prepare_comparison_data(audio_df, year1, year2, features):
    """
    Prepare comparison data for two years.
    
    Args:
        audio_df: DataFrame with audio features
        year1: first year to compare
        year2: second year to compare
        features: list of features to compare
        
    Returns:
        DataFrame with Feature, Year, and Value columns
    """
    # filtering data for each year
    audio_df_year1 = audio_df[audio_df['year'] == year1][features].mean()
    audio_df_year2 = audio_df[audio_df['year'] == year2][features].mean()
    
    # creating a DataFrame for comparison
    comparison_audio_df = pd.DataFrame({
        'Feature': features,
        str(year1): audio_df_year1.values,
        str(year2): audio_df_year2.values
    }).melt(id_vars=['Feature'], var_name='Year', value_name='Value')
    
    return comparison_audio_df

def filter_year_data(audio_df, track_df, year1, year2, features):
    """
    Filter and calculate means for two selected years.
    
    Args:
        audio_df: DataFrame with audio features
        track_df: DataFrame with track features
        year1: first year to compare
        year2: second year to compare
        features: list of features to analyze
    
    Returns:
        tuple: (audio_df_year1_mean, audio_df_year2_mean, track_df_year1, track_df_year2)
    """
    # Calculate means for audio features
    audio_df_year1 = audio_df[audio_df['year'] == year1][features].mean()
    audio_df_year2 = audio_df[audio_df['year'] == year2][features].mean()
    
    # Filter track data
    track_df_year1 = track_df[audio_df['year'] == year1]
    track_df_year2 = track_df[audio_df['year'] == year2]
    
    return audio_df_year1, audio_df_year2, track_df_year1, track_df_year2

def three_random_tracks(track_df):
    """
    Get three random tracks from the track DataFrame.
    
    Args:
        track_df: DataFrame with track information
        
    Returns:
        tuple: (song1, song2, song3, artist1, artist2, artist3, 
                url1, url2, url3, cover1, cover2, cover3)
    """
    # Get random track indices
    random_tracks = track_df.sample(3)
    
    # Get track information
    song1, song2, song3 = random_tracks['song_name'].tolist()
    artist1, artist2, artist3 = random_tracks['artist_name'].tolist()
    url1, url2, url3 = random_tracks['spotify_url'].tolist()
    cover1, cover2, cover3 = random_tracks['cover_image'].tolist()
    
    return (song1, song2, song3, 
            artist1, artist2, artist3,
            url1, url2, url3,
            cover1, cover2, cover3)


def filter_spotify_by_year(dataframe, start_year, end_year):
    """
    Filter Spotify data by year range.
    
    Args:
        dataframe: DataFrame with chart positions
        start_year: int, starting year for filter
        end_year: int, ending year for filter
        
    Returns:
        DataFrame with filtered Spotify ids
    """
    # Convert chart_week to int
    dataframe['chart_week'] = pd.to_numeric(dataframe['chart_week'])
    
    filtered_spotify_data = dataframe[
        (dataframe['chart_week'] >= start_year) & 
        (dataframe['chart_week'] <= end_year)
    ]
    
    # get three random tracks
    three_random_tracks = filtered_spotify_data.sample(n=3)
    
    return three_random_tracks