import os 
import pandas as pd
from dotenv import load_dotenv
from requests import post, get
import base64
import json
from data_loading import bigquery_authenticate, load_data, get_token


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
    
    return merged_dataframe


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
        'valence': 'mean'
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

# getting three top rated songs from each year
def three_random_songs(dataframe):
    
    # sorting by list_position 1 to get top rated songs
    sorted_dataframe = dataframe[dataframe['list_position'] == 1]
    
    # grouping by year and taking 3 random entries from each year
    random_three = (sorted_dataframe
        .groupby(sorted_dataframe['chart_week'].dt.year)
        .apply(lambda x: x.sample(n=min(len(x), 3)))
        .reset_index(drop=True)
    )
    
    # drop list_position
    random_three = random_three.drop('list_position', axis=1)
    
    return random_three


# fetching data from spotify api
def fetch_and_parse_spotify_data(dataframe):
    # getting access token for authentication
    token = get_token()
    
    # placeholder for parsed data
    parsed_song_data = []

    # iterate over dataframe rows to get both track_id and chart_week
    for index, row in dataframe.iterrows():
        # constructing the URL and headers for GET request
        url = f'https://api.spotify.com/v1/tracks/{row["track_id"]}'
        headers = {'Authorization': 'Bearer ' + token}
        
        # making the GET request
        response = get(url, headers=headers)
        data = response.json()
        
        # create clean song data with chart_week
        clean_song_data = {
            'chart_week': row['chart_week'],
            'song_name': data['name'],
            'artist_name': data['album']['artists'][0]['name'],
            'spotify_url': data['external_urls']['spotify'],
            'cover_image': data['album']['images'][0]['url']
        }
        parsed_song_data.append(clean_song_data)
    
    # create DataFrame from parsed data
    return pd.DataFrame(parsed_song_data)