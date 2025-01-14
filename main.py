# importing functions for data loading and processing 
from load_data import bigquery_authenticate, load_data
from data_processing import drop_duplicates, convert_to_datetime, merge_chart_audio_features, aggregate_audio_features, merge_chart_track_features, aggregate_track_features
import os 
import pandas as pd

# authenticating to bigquery
client = bigquery_authenticate()

# loading data from bigquery
audio_features = load_data(client,'audio_features')
chart_positions = load_data(client, 'chart_positions')
tracks = load_data(client, 'tracks')

# cleaning data 
audio_features_clean = drop_duplicates(audio_features)
tracks_clean = drop_duplicates(tracks)
chart_positions_clean = convert_to_datetime(chart_positions)

# merging chart positions with audio features 
first_merge = merge_chart_audio_features(chart_positions_clean, audio_features_clean)

# merging charts with tracks
second_merge = merge_chart_track_features(first_merge, tracks_clean)

# aggregate data
aggregated_audio_features = aggregate_audio_features(first_merge)
aggregated_track_features = aggregate_track_features(second_merge)

# create a new folder named "data_backup" in the current directory
folder_name = 'data'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    
# saving clean files in "data"
aggregated_audio_features.to_csv(os.path.join(folder_name, 'audio_data.csv'), index=False)
aggregated_track_features.to_csv(os.path.join(folder_name, 'track_data.csv'), index=False)