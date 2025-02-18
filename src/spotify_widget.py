import streamlit as st
import base64
import json
from requests import post, get
import pandas as pd 
 
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



# fetching data from spotify api
def fetch_and_parse_spotify_songs(track_ids, token, client_id, client_secret):
    """
    Fetch and parse track data from Spotify API
    
    Args:
        track_ids: str or list of str - Spotify track ID(s)
        token: str - Spotify API token
        client_id: str - Spotify client ID
        client_secret: str - Spotify client secret
    
    Returns:
        pd.DataFrame with columns: song_name, artist_name, spotify_url, cover_image
    """
    # Convert single track_id to list
    if isinstance(track_ids, str):
        track_ids = [track_ids]
    
    # placeholder for parsed data
    parsed_song_data = []

    # iterate over track IDs
    for track_id in track_ids:
        # constructing the URL and headers for GET request
        url = f'https://api.spotify.com/v1/tracks/{track_id}'
        headers = {'Authorization': 'Bearer ' + token}
        
        # making the GET request
        response = get(url, headers=headers)
        data = response.json()
        
        # create clean song data
        clean_song_data = {
            'track_id': track_id,
            'song_name': data['name'],
            'artist_name': data['album']['artists'][0]['name'],
            'spotify_url': data['external_urls']['spotify'],
            'cover_image': data['album']['images'][0]['url']
        }
        parsed_song_data.append(clean_song_data)
    
    # create DataFrame from parsed data
    return pd.DataFrame(parsed_song_data)

# fetching artist data from spotify api
def fetch_and_parse_spotify_artist_data(id, token, client_id, client_secret):
    
    # placeholder for parsed data
    parsed_song_data = []
    
    # constructing the URL and headers for GET request
    url = f'https://api.spotify.com/v1/artists/{id}'
    headers = {'Authorization': 'Bearer ' + token}
    
    # making the GET request
    response = get(url, headers=headers)
    data = response.json()
    
    # get image URL safely
    image_url = data['images'][0]['url'] if data.get('images') and len(data['images']) > 0 else None
    
    # create clean song data with chart_week
    clean_song_data = {
        'artist_name': data['name'],
        'popularity': data['popularity'],
        'followers': data['followers']['total'],
        'spotify_url': data['external_urls']['spotify'],
        'artist_image': image_url
    }
    parsed_song_data.append(clean_song_data)
    
    # create DataFrame from parsed data
    return pd.DataFrame(parsed_song_data)
 
# displaying artist data
def show_spotify_artist_components(dataframe):
    
    # Extract values from DataFrame (taking first row since we expect single artist)
    artist_name = dataframe['artist_name'].iloc[0]
    artist_image = dataframe['artist_image'].iloc[0]
    followers = dataframe['followers'].iloc[0]
    popularity = dataframe['popularity'].iloc[0]
    spotify_url = dataframe['spotify_url'].iloc[0]
    
    st.image(artist_image, use_column_width=False, width=100)
    
    st.write("") 
    
    # Display artist info
    st.subheader(artist_name)
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Spotify Followers", f"{followers:,}")
    with col2:
        st.metric("Popularity Popularity", f"{popularity}/100")
    
    st.write("") 
    st.link_button('Go to Spotify profile', spotify_url)

   

    

    
    

    







