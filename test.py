  

    
def test():   

    client = bigquery_authenticate()  
    
    # loading data from bigquery
    audio_features = load_data(client,'audio_features')
    chart_positions = load_data(client, 'chart_positions')
    tracks = load_data(client, 'tracks')

    # cleaning data from bigquery
    audio_features_clean = drop_duplicates(audio_features)
    tracks_clean = drop_duplicates(tracks)
    chart_positions_clean = convert_to_datetime(chart_positions)

    # merging and cleaning tables to get all necessary field for app
    first_merge = merge_chart_audio_features(chart_positions_clean, audio_features_clean)
    second_merge = merge_chart_track_features(first_merge, tracks_clean)

    # aggregate tables for app
    audio_df = aggregate_audio_features(first_merge)
    track_df = aggregate_track_features(second_merge)
    spotify_df = select_spotify_tracks(second_merge)
    
    return audio_df, track_df, spotify_df