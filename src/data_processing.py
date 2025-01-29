import os 
import pandas as pd
from dotenv import load_dotenv
from requests import post, get
import base64
import json

# drop duplicates from dataframe
def drop_duplicates(dataframe):
    
    import pandas as pd
    
    # saving duplicates to list  
    duplicates_list = dataframe.loc[dataframe.duplicated()].index 
    
    # dropping duplicates and resetting index
    dataframe.drop(duplicates_list, inplace=True)
    dataframe.reset_index(drop= True, inplace= True)
    
    # dropping empty rowan and reseting index
    dataframe.drop(0, inplace=True)
    dataframe.reset_index(drop= True, inplace= True)
    
    return dataframe

# convert data chart_week column to datetime object 
def convert_to_datetime(dataframe):
    
    import pandas as pd
    
    # converting chart_week column in chart_positions table from string to datetime for convenient filtering down the line 
    dataframe['chart_week'] = pd.to_datetime(dataframe['chart_week'])
    
    return dataframe

# merging charts with audio features
def merge_chart_audio_features(chart_dataframe, audio_features_dataframe):
    
    import pandas as pd
    
    # creating chart with audio features by merging chart_positions with tracks on 'track_id'
    merged_dataframe = pd.merge(chart_dataframe, audio_features_dataframe, on='track_id', how= 'left')
    merged_dataframe.dropna(inplace=True)
    
    # rename column
    merged_dataframe = merged_dataframe.rename(columns={'chart_week': 'year'})
    
    return merged_dataframe

# merging charts with tracks 
def merge_chart_track_features(chart_dataframe, track_dataframe):
    
    import pandas as pd
    
    #merging chart_dataframe with track artist mapping
    merged_dataframe = pd.merge(chart_dataframe, track_dataframe, on='track_id', how= 'inner')
    
    # filter rows where release_date is before year (year = year that the song was featured on a chart)
    filtered_dataframe = merged_dataframe[merged_dataframe['release_date'] < merged_dataframe['year']]
    
    return filtered_dataframe

# aggregates data by year
def aggregate_audio_features(dataframe):
    
    import pandas as pd
    
    # extracting year and aggregating values for each year
    agg_df = dataframe.groupby(dataframe['year'].dt.year).agg({
        'danceability': 'mean',
        'energy': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'valence': 'mean',
        'speechiness': 'mean'
    }).reset_index()
    
    return agg_df

# aggregates data by year
def aggregate_track_features(dataframe):
    
    import pandas as pd      
    
    # extracting year and aggregating values for each year
    agg_df = dataframe.groupby(dataframe['year'].dt.year).agg({
        'loudness': 'mean', 
        'tempo': 'mean',
        'duration_ms':'mean', 
    }).reset_index()
    
    agg_df['loudness'] = round(agg_df['loudness'])
    agg_df['tempo'] = round(agg_df['tempo'])
    agg_df['duration_ms'] = round(agg_df['duration_ms'] / 60000, 2)

    # rename columns
    agg_df = agg_df.rename(columns={
        'loudness': 'Loudness (dB)',
        'tempo': 'Tempo (BPM)',
        'duration_ms': 'Duration (min)'
    })
    return agg_df

# select spotify tracks that were released before they were featured on a chart and had a list position of 1
def select_spotify_tracks(dataframe):
    # filter on rows where list potion is 1
    filtered_top_songs = dataframe[dataframe['list_position'] == 1]

    return filtered_top_songs

def merge_artist_features(tracks, mapping, artists):

    artist_track = pd.merge(mapping, tracks, how='inner', on='track_id')
    artist_track_ = pd.merge(artists, artist_track, how='inner', on='artist_id')

    return artist_track_

def process_artist_data(artist_name, artist_track_, audio_features):
    """
    Process data for a given artist name to calculate charts and audio features.

    Args:
        artist_name (str): Name of the artist.
        artist_track_chart (pd.DataFrame): DataFrame with artist and track chart data.
        chart (pd.DataFrame): DataFrame with chart data.
        audio_features (pd.DataFrame): DataFrame with audio features.

    Returns:
        tuple: A tuple containing:
            - artist_charts (pd.DataFrame): DataFrame with artist chart data.
            - artist_features (pd.DataFrame): DataFrame with artist features.
            - artist_features_mean (pd.DataFrame): DataFrame with mean features for the artist.
    """

    artist_data = artist_track_[artist_track_['name_x'] == artist_name].groupby(['track_id'])
    artist_data = pd.DataFrame(artist_data)

    artist_mapped = artist_data[0].map(lambda x: x[0])
    artist_mapped = pd.DataFrame(artist_mapped)
    artist_features_ = pd.merge(artist_mapped, audio_features, left_on=0, right_on='track_id', how='inner')
    artist_features_mean = artist_features_.agg({
        'danceability': 'mean',
        'energy': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'valence': 'mean',
        'speechiness': 'mean',
        'key': 'mean',
        'mode': 'mean',
        'tempo': 'mean',
        'time_signature': 'mean',
    }).reset_index()
    artist_features_mean['name'] = artist_name

    return artist_features_mean

def data_to_radar_chart(*tables):
    """
    Concatenate any number of DataFrames into a radar chart table.

    Args:
        *tables: One or more pandas DataFrames, each having 'name', 'index', and 0 as columns.

    Returns:
        pd.DataFrame: A single DataFrame created by concatenating all input tables.
    """
    # Convert each input table using pivot_table
    pivoted_tables = [
        table.pivot_table(index='name', columns='index', values=0, aggfunc='first').reset_index()
        for table in tables
    ]

    # Concatenate all pivoted tables
    radar_table = pd.concat(pivoted_tables, ignore_index=True)

    return radar_table

def prepare_artist_data(tracks, mapping, artists):
    
    artist_track = pd.merge(mapping, tracks, how='inner', on = 'track_id')
    artist_track_ = pd.merge(artists, artist_track, how='inner', on = 'artist_id')
    
    return artist_track_

def data_to_radar_chart(*tables):
    """
    Concatenate any number of DataFrames into a radar chart table.

    Args:
        *tables: One or more pandas DataFrames, each having 'name', 'index', and 0 as columns.

    Returns:
        pd.DataFrame: A single DataFrame created by concatenating all input tables.
    """
    # Convert each input table using pivot_table
    pivoted_tables = [
        table.pivot_table(index='name', columns='index', values=0, aggfunc='first').reset_index()
        for table in tables
    ]
    
    # Concatenate all pivoted tables
    radar_table = pd.concat(pivoted_tables, ignore_index=True)
    
    return radar_table

def get_trending_artists(tracks, mapping, artists, charts):
    
    track_chart = pd.merge(tracks, charts, how='inner', on='track_id')
    artist_track = pd.merge(mapping, track_chart, how='inner', on = 'track_id')
    artist_track_ = pd.merge(artists, artist_track, how='inner', on = 'artist_id')
    
    return artist_track_

def calculate_trend_changes(audio_df, year, features):
    trend_changes = {"feature": [], "change": []}
    
    for feature in features:
        avg_feature_base = audio_df[feature].mean()
        avg_feature_current = audio_df[audio_df['year'] == year][feature].mean()
        change =  avg_feature_base - avg_feature_current

        trend_changes["feature"].append(feature)
        trend_changes["change"].append(change)

    return trend_changes