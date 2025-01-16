#import pandas as pd 

# Authenticate to GCP


# authenticating to bigquery
def bigquery_authenticate():
    # Authenticate to GCP
    from google.auth import load_credentials_from_file
    from google.cloud.bigquery import Client
    
    # accessing bigquery credentials from local file 
    credentials, project_id = load_credentials_from_file('service_account.json')
    
    # Load data from BigQuery
    client = Client(
        project = project_id,
        credentials = credentials
)
    return client

client = bigquery_authenticate()

# creating a data loading function 
def load_data(client, table): 
    # selecting table
    query = f"SELECT * FROM `da26-python.music_data.{table}`" 
    # creating query job and transforming to dataframe  
    load_job = client.query(query)
    data = load_job.to_dataframe() 
    # return dataframe 
    return data


#def load_csv_data():
    """
    Load preprocessed data from CSV files.
    
    Returns:
        tuple: (audio_df, track_df, spotify_df)
    """

    audio_df = pd.read_csv('data/audio_data.csv')
    track_df = pd.read_csv('data/track_data.csv')
    spotify_df = pd.read_csv('data/spotify_data.csv')
    
    return audio_df, track_df, spotify_df


