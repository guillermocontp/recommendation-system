import os
from dotenv import load_dotenv
from requests import post, get
import base64
import json

# Authenticate to GCP
from google.auth import load_credentials_from_file
from google.cloud.bigquery import Client

# authenticating to bigquery
def bigquery_authenticate():
    # Authenticate to GCP
    #from google.auth import load_credentials_from_file
    #from google.cloud.bigquery import Client
    
    # accessing bigquery credentials from local file 
    credentials, project_id = load_credentials_from_file('service_account.json')
    
    # Load data from BigQuery
    client = Client(
        project = project_id,
        credentials = credentials
)
    return client

# creating a data loading function 
def load_data(client, table): 
    # selecting table
    query = f"SELECT * FROM `da26-python.music_data.{table}`" 
    # creating query job and transforming to dataframe  
    load_job = client.query(query)
    data = load_job.to_dataframe() 
    # return dataframe 
    return data


# getting access token from Spotify API
def get_token(client_id, client_secret):
    
    # constructing authentication credentials
    auth_string = client_id + ":" + client_secret
    # encoding the credentials to base64
    auth_bytes = auth_string.encode('utf-8')
    # converting the bytes to a string
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    # making a POST request to the Spotify API to get the access token
    url = "https://accounts.spotify.com/api/token"
    
    # constructing the headers and data for the POST request
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # defining data as clint credentials
    data = {'grant_type': 'client_credentials'}
    
    # making the POST request
    result = post(url, headers = headers, data = data)
    # converting the result to a json object
    json_results = json.loads(result.content)
    # getting the access token from the json object
    token = json_results['access_token']
    
    # returning access token
    return token    