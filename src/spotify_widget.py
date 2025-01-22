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
    
    st.image(artist_image, use_column_width=False, width=300)
    
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

   
# displaying artist data
def show_spotify_comparison_components(dataframe1, dataframe2):
    
    # Extract values from DataFrame (taking first row since we expect single artist)
    artist_name1 = dataframe1['artist_name'].iloc[0]
    artist_image1 = dataframe1['artist_image'].iloc[0]
    followers1 = dataframe1['followers'].iloc[0]
    popularity1 = dataframe1['popularity'].iloc[0]
    spotify_url1 = dataframe1['spotify_url'].iloc[0]
    
    artist_name2 = dataframe2['artist_name'].iloc[0]
    artist_image2 = dataframe2['artist_image'].iloc[0]
    followers2 = dataframe2['followers'].iloc[0]
    popularity2 = dataframe2['popularity'].iloc[0]
    spotify_url2 = dataframe2['spotify_url'].iloc[0]
    
    col1, spacer, col2 = st.columns([2, 0.25, 2])
    with col1:
        st.image(artist_image1, use_column_width=False, width=250)
        st.write("") 
        st.subheader(artist_name1)
        st.metric("Spotify Followers", f"{followers1:,}")
        st.metric("Popularity Popularity", f"{popularity1}/100")
        st.write("") 
        st.link_button('Go to Spotify profile', spotify_url1)
        
    with col2:
        st.image(artist_image2, use_column_width=False, width=250)
        st.write("") 
        st.subheader(artist_name2)
        st.metric("Spotify Followers", f"{followers2:,}")
        st.metric("Popularity Popularity", f"{popularity2}/100")
        st.write("") 
        st.link_button('Go to Spotify profile', spotify_url2)
    

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

    
def show_spotify_components_min_max(max_dataframe, min_dataframe, selected_feature):
    cover1 = max_dataframe['cover_image'].values[0]
    song1 = max_dataframe['song_name'].values[0]
    artist1 = max_dataframe['artist_name'].values[0]
    url1 = max_dataframe['spotify_url'].values[0]
    
    cover2 = min_dataframe['cover_image'].values[0]
    song2 = min_dataframe['song_name'].values[0]
    artist2 = min_dataframe['artist_name'].values[0]
    url2 = min_dataframe['spotify_url'].values[0]
    
    # max song 
    
    st.markdown(f"**Song with highest {selected_feature}**")
    st.write("") 
    st.image(cover1, use_column_width=False, width=150)
    st.markdown(f"**{song1}**<br>{artist1}", unsafe_allow_html=True)
    st.link_button('Listen on Spotify', url1)
    st.write("") 
 
    # min song
    st.markdown(f"**Song with lowest {selected_feature}**")
    st.write("") 
    st.image(cover2, use_column_width=False, width=150)
    st.markdown(f"**{song2}**<br>{artist2}", unsafe_allow_html=True)
    st.link_button('Listen on Spotify', url2) 
    st.write("") 
    
    
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

def filter_spotify_by_year_and_feature(start_year, end_year, top_list, feature):
    
    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # Extract year from datetime for comparison
    filtered_top_list = top_list[
        (top_list['year'].dt.year >= int(start_year)) & 
        (top_list['year'].dt.year <= int(end_year))
    ]
   
    # gets song with highest value for selected feature 
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    filter_on_feature = unique_songs.sort_values(by=feature, ascending=False)
    max_song = filter_on_feature.head(1)
    

    # gets song with lowest value for selected feature 
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    filter_on_feature = unique_songs.sort_values(by=feature, ascending=True)
    min_song = filter_on_feature.head(1)
    
    return max_song, min_song

def filter_spotify_by_single_year(year, top_list):

    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # extract year from datetime 
    filtered_top_list = top_list[
        (top_list['year'].dt.year == int(year))
    ]
    
    # sample 3 random unique songs
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    three_random_songs = unique_songs.sample(3)
    
    return three_random_songs

def filter_spotify_by_single_year_and_feature(year, top_list, feature):
    # convert chart_week to datetime
    top_list['year'] = pd.to_datetime(top_list['year'])

    # extract year from datetime 
    filtered_top_list = top_list[
        (top_list['year'].dt.year == int(year))
    ]
    
    # get unique songs
    unique_songs = filtered_top_list.groupby('track_id').first().reset_index()
    
    # sort by feature to get max and min
    filter_on_feature = unique_songs.sort_values(by=feature, ascending=False)
    
    # get max and min songs
    max_song = filter_on_feature.head(1)
    min_song = filter_on_feature.tail(1)
    
    return max_song, min_song

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