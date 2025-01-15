import pandas as pd 

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