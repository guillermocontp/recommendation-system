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
def fetch_and_parse_spotify_data(dataframe, token, client_id, client_secret):
    
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
            'year': row['year'],
            'song_name': data['name'],
            'artist_name': data['album']['artists'][0]['name'],
            'spotify_url': data['external_urls']['spotify'],
            'cover_image': data['album']['images'][0]['url']
        }
        parsed_song_data.append(clean_song_data)
    
    # create DataFrame from parsed data
    return pd.DataFrame(parsed_song_data)
 
   
def get_spotify_components(dataframe):
    """
    Load first 3 tracks' data from dataframe.
    
    Args:
        dataframe: DataFrame containing track information
        
    Returns:
        tuple: (song1, song2, song3, artist1, artist2, artist3, 
               url1, url2, url3, cover1, cover2, cover3)
    """
    # Create lists for each feature
    songs = dataframe['song_name'].tolist()
    artists = dataframe['artist_name'].tolist()
    urls = dataframe['spotify_url'].tolist()
    covers = dataframe['cover_image'].tolist()
    
    # Get first 3 items from each list
    song1, song2, song3 = songs[:3]
    artist1, artist2, artist3 = artists[:3]
    url1, url2, url3 = urls[:3]
    cover1, cover2, cover3 = covers[:3]
    
    return (song1, song2, song3, 
            artist1, artist2, artist3,
            url1, url2, url3,
            cover1, cover2, cover3)
    
def show_spotify_components(song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3):
    
    st.image(cover1, use_column_width=False, width=150)
    st.markdown(f"**{song1}**<br>{artist1}", unsafe_allow_html=True)
    st.link_button('Listen on Spotify', url1)
    st.write("") 
 

    st.image(cover2, use_column_width=False, width=150)
    st.markdown(f"**{song2}**<br>{artist2}", unsafe_allow_html=True)
    st.link_button('Listen on Spotify', url2) 
    st.write("") 
    
    st.image(cover3, use_column_width=False, width=150)
    st.markdown(f"**{song3}**<br>{artist3}", unsafe_allow_html=True)
    st.link_button('Listen on Spotify', url3)  
    st.write("") 
    
    
def filter_spotify_by_year(start_year, end_year, top_list):
    
    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # Extract year from datetime for comparison
    filtered_top_list = top_list[
        (top_list['year'].dt.year >= int(start_year)) & 
        (top_list['year'].dt.year <= int(end_year))
    ]
    
    # Sample 3 random unique songs
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    three_random_songs = unique_songs.sample(3)
    
    return three_random_songs

def filter_spotify_by_single_year(year, top_list):

    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # extract year from datetime 
    filtered_top_list = top_list[
        (top_list['year'].dt.year == int(year))
    ]
    
    # Sample 3 random unique songs
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    three_random_songs = unique_songs.sample(3)
    
    return three_random_songs

def filter_spotify_for_comparison(year1, year2, top_list):

    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # extract year1 from datetime for comparison
    year1_filtered_top_list = top_list[
        (top_list['year'].dt.year == int(year1))
    ]

    # extract year1 from datetime for comparison
    year2_filtered_top_list = top_list[
        (top_list['year'].dt.year == int(year2))
    ]
    
    # Sample 3 random unique songs
    year1_unique_songs = year1_filtered_top_list.groupby('track_id').first().reset_index()
    year1_three_random_songs = year1_unique_songs.sample(3)
    
    year2_unique_songs = year2_filtered_top_list.groupby('track_id').first().reset_index()
    year2_three_random_songs = year2_unique_songs.sample(3)
    
    return year1_three_random_songs, year2_three_random_songs