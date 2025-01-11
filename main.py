# takes DataFrame as argument
# performs aggregations and returns two DataFrames for visualization
def return_audio_features(dataframe):
    
    import pandas as pd
    
    # placeholder lists for DataFrames
    chart_data = []
    numerical_data = []
    
    # aggregating values for barchart 
    features_dict = {
        # get value for audio features (value range from 0-1)
        'danceability': dataframe['danceability'].mean(),
        'energy': dataframe['energy'].mean(),
        'mode': dataframe['mode'].mean(),
        'speechiness': dataframe['speechiness'].mean(),
        'acousticness': dataframe['acousticness'].mean(),
        'instrumentalness': dataframe['instrumentalness'].mean(),
        'liveness': dataframe['liveness'].mean(),
        'valence': dataframe['valence'].mean(),
    }
        
    # find most frequent key in the dataset
    most_frequent_key = int(round(dataframe['key'].mode().iloc[0]))
        
    # keys are represented as integers (0-11) corresponding to musical notes
    keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    key = keys[most_frequent_key]
        
    # aggregating values for numerical presentation 
    numerical_dict = {
        # get average beats per minute 
        'average_bpn': round(dataframe['tempo'].mean()),
        # get average beats per bar 
        'average_beats_per_bar': round(dataframe['time_signature'].mean()),
        # get precentage of songs in major and minor 
        'percentage_of_major': round((dataframe['mode'] == 1).mean() * 100),
        'percentage_of_minor': round((dataframe['mode'] == 0).mean() * 100),
        # get most requent key 
        'most_requent_key': key,
        # get average decibel 
        'average_decibels': round(dataframe['loudness'].mean())
    }
    
    # create two coloumns for barchart
    chart_data = {
        'feature': list(features_dict.keys()),
        'value': list(features_dict.values())
    }
    
    # create two coloumns for numerical data
    numerical_data = {
        'metric': list(numerical_dict.keys()),
        'value': list(numerical_dict.values())
    }
    
    # create DataFrames from dictionarys 
    chart_df = pd.DataFrame(chart_data)
    numerical_df = pd.DataFrame(numerical_data)
    
    return chart_df, numerical_df
    
    
    
# takes two DataFrames as arguments, returns barplot (Spotify-inspired) and list of audio features
def show_audio_features(feature_df, metric_df):
    
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(figsize=(12, 6))

    # create barplot
    sns.barplot(data=feature_df, 
            x='feature', 
            y='value')
    
   # set y-axis limit
    plt.ylim(0, 1.0)
    # Create tick range
    ticks = [x/10 for x in range(0, 11)]
    plt.yticks(ticks)

    plt.tight_layout()
    plt.show()

    # get values from numerical data
    bpn = metric_df.iloc[0,1]
    bppb = metric_df.iloc[1,1]
    major = metric_df.iloc[2,1]
    minor = metric_df.iloc[3,1]
    key = metric_df.iloc[4,1]
    db = metric_df.iloc[5,1]
    
    # return list with numerical values
    return [
    f'The average beat per minute is: {bpn}',
    f'The average beat per bar is: {bppb}',
    f'The average decibel is: {db}',
    f'The precentage of songs in major is: {major}',
    f'The precentage of songs in minor is: {minor}',
    f'Most songs are in key: {key}'
    ]
    
    
def analyze_seasonal_trends(df):
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Extract month from chart_week
    df['month'] = pd.to_datetime(df['chart_week']).dt.month
    
    # Select features to analyze
    features = ['energy', 'mode', 'danceability', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    
    # Calculate monthly averages
    monthly_trends = df.groupby('month')[features].agg({
        'danceability': 'mean',
        'energy': 'mean',
        'mode': 'mean',
        'speechiness': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'valence': 'mean',
    }).round(2)
    
    # Plot trends
    plt.figure(figsize=(12, 6))
    for feature in features:
        plt.plot(monthly_trends.index, monthly_trends[feature], 
                label=feature, marker='o')
    
    plt.title('Seasonal Trends in Musical Features')
    plt.xlabel('Month')
    plt.ylabel('Average Value')
    plt.legend()
    plt.grid(True)
    
    return monthly_trends


# takes DataFrame as argument
# performs aggregations and returns two DataFrames for visualization
def return_audio_features(dataframe):
    
    # placeholder lists for DataFrames
    chart_data = []
    numerical_data = []
    
    # aggregating values for barchart 
    features_dict = {
        # get value for audio features (value range from 0-1)
        'danceability': dataframe['danceability'].mean(),
        'energy': dataframe['energy'].mean(),
        'mode': dataframe['mode'].mean(),
        'speechiness': dataframe['speechiness'].mean(),
        'acousticness': dataframe['acousticness'].mean(),
        'instrumentalness': dataframe['instrumentalness'].mean(),
        'liveness': dataframe['liveness'].mean(),
        'valence': dataframe['valence'].mean(),
    }
        
    # find most frequent key in the dataset
    most_frequent_key = int(round(dataframe['key'].mode().iloc[0]))
        
    # keys are represented as integers (0-11) corresponding to musical notes
    keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    key = keys[most_frequent_key]
        
    # aggregating values for numerical presentation 
    numerical_dict = {
        # get average beats per minute 
        'average_bpn': round(dataframe['tempo'].mean()),
        # get average beats per bar 
        'average_beats_per_bar': round(dataframe['time_signature'].mean()),
        # get precentage of songs in major and minor 
        'percentage_of_major': round((dataframe['mode'] == 1).mean() * 100),
        'percentage_of_minor': round((dataframe['mode'] == 0).mean() * 100),
        # get most requent key 
        'most_requent_key': key,
        # get average decibel 
        'average_decibels': round(dataframe['loudness'].mean())
    }
    
    # create two coloumns for barchart
    chart_data = {
        'feature': list(features_dict.keys()),
        'value': list(features_dict.values())
    }
    
    # create two coloumns for numerical data
    numerical_data = {
        'metric': list(numerical_dict.keys()),
        'value': list(numerical_dict.values())
    }
    
    # create DataFrames from dictionarys 
    chart_df = pd.DataFrame(chart_data)
    numerical_df = pd.DataFrame(numerical_data)
    
    return chart_df, numerical_df
    