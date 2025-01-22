# importing necessary libraries
import streamlit as st
import os
from dotenv import load_dotenv

# importing necessary functions from src
from src.data_processing import (
    process_artist_data,
    data_to_radar_chart,
)
from src.visualization import (
    create_radar_chart_new
)
from src.spotify_widget import (
    get_token,
    fetch_and_parse_spotify_artist_data,
    show_spotify_artist_components,
    show_spotify_comparison_components   
)

from src.filter import (
    create_year_sidebar_filters,
    filter_artist_by_years
)
from home import load_and_cache

audio_df, track_df, spotify_songs, mapping, artists, artist_track_, audio_features, trending_artists = load_and_cache()

# loading Spotify credentials (for API) from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = get_token(client_id, client_secret)

# defining start and end year 
#features, avg_data = initialize_features_and_averages(track_df, audio_df)

# creating sidebar filters
with st.sidebar:
    st.title("Filters")
    
    # selectbox for artist comparison
    artist_option = st.sidebar.selectbox(
        'Select view:',
        ('Trending', 'Specific', 'Comparison'), key="artist_comparison"
    )
       
    # if user selects specific artist, show search field
    if artist_option == 'Specific':
    
        artist_list = sorted(artist_track_['name_x'].unique())

        selected_artist = st.selectbox(
            "Search for an artist",
            options=artist_list,
            index=None,
            placeholder="Type artist name..."
        )
    
    # if user selects specific artist, show search fields
    if artist_option == 'Comparison':
        
        artist_list = sorted(artist_track_['name_x'].unique())

        # create searchable dropdown
        first_artist = st.selectbox(
            "Search for first artist",
            options=artist_list,
            index=None,
            placeholder="Type artist name..."
        ) 
        
        # create searchable dropdown
        second_artist = st.selectbox(
            "Search for second artist",
            options=artist_list,
            index=None,
            placeholder="Type artist name..."
        ) 

# defining trending artists
#list_of_trending = trending_artists.groupby(['name_x'])['explicit'].count().nlargest(10)

# creating columns
col1, spacer, col2 = st.columns([2.5, 0.5, 2])

# if user selects trending artists
if artist_option == 'Trending':
    
    # create filter selectbox for year range
    start_year, end_year = create_year_sidebar_filters(audio_df)
    
    # defining trending artists
    filtered_trending_artists = filter_artist_by_years(trending_artists, start_year, end_year)
    list_of_trending = filtered_trending_artists.groupby(['name_x'])['explicit'].count().nlargest(10)
    
    # selectbox for trending artists
    option = st.sidebar.selectbox(
    "Choose an artist",
    (list_of_trending.index))

    # fetch and snow artist information
    with col1:
        st.header('Artist Profile')
        st.markdown("---")
        st.write("")
        
        # filtering on selected artist
        artist_match = artist_track_[artist_track_['name_x'] == option]
        artist_id = artist_match['artist_id']
        artist_id = artist_id.iloc[0]

        # fetching and visualizing artist data
        fetched_song = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)
        show_spotify_artist_components(fetched_song)
    
    # visualize artist audio profile
    with col2:
        st.header('Artist Audio Profile')
        st.markdown("---")

        # visualizing artist audio profile
        artist1_mean = process_artist_data(option, artist_track_, audio_features)
        data_radar = data_to_radar_chart(artist1_mean)
        fig = create_radar_chart_new(data_radar)
        st.plotly_chart(fig, use_container_width=True)
        
# if user selects trending artists
if artist_option == 'Specific':
    
    # fetch and snow artist information
    with col1:
        st.header('Artist Profile')
        st.markdown("---")
        st.write("")
        
        # error handling if no artist is selected
        if selected_artist == None:
            st.write("Please select an artist")
        else:
            artist_match = artist_track_[artist_track_['name_x'] == selected_artist]   
            artist_id = artist_match['artist_id']
            
            artist_id = artist_id.values[0]

            test_fetch = fetch_and_parse_spotify_artist_data(artist_id, token, client_id, client_secret)
            show_spotify_artist_components(test_fetch)     

    # visualize artist audio profile
    with col2:
        st.header('Artist Audio Profile')
        st.markdown("---")
        
        # error handling if no artist is selected
        if selected_artist == None:
            st.write("Please select an artist")
        else:
            artist1_mean = process_artist_data(selected_artist, artist_track_, audio_features)
            data_radar = data_to_radar_chart(artist1_mean)
            fig = create_radar_chart_new(data_radar)
            st.plotly_chart(fig, use_container_width=True)

# if user select comparison
if artist_option == 'Comparison':

    # fetch and snow artists data
    with col1:
        st.header('Artist Profile')
        st.markdown("---")
        st.write("")
        
        # error handling if no artist is selected
        if first_artist == None or second_artist == None:
            st.write("Please select an artist") 
        else:
            first_artist_match = artist_track_[artist_track_['name_x'] == first_artist]   
            first_artist_id = first_artist_match['artist_id']
            
            first_artist_id = first_artist_id.values[0]

            first_artist_fetch = fetch_and_parse_spotify_artist_data(first_artist_id, token, client_id, client_secret)
            
            second_artist_match = artist_track_[artist_track_['name_x'] == second_artist]   
            second_artist_id = second_artist_match['artist_id']
            
            second_artist_id = second_artist_id.values[0]

            second_artist_fetch = fetch_and_parse_spotify_artist_data(second_artist_id, token, client_id, client_secret)
                        
            show_spotify_comparison_components(first_artist_fetch, second_artist_fetch)
    
    # visualize artist audio profile
    with col2:
        st.header('Artist Audio Profile')
        st.markdown("---")
        
        # error handling if no artist is selected
        if first_artist == None or second_artist == None:
            st.write("Please select an artist")
        else:
            artist1_mean = process_artist_data(first_artist, artist_track_, audio_features)
            artist2_mean = process_artist_data(second_artist, artist_track_, audio_features)
        
            data_radar = data_to_radar_chart(artist1_mean, artist2_mean)
            fig = create_radar_chart_new(data_radar)
            st.plotly_chart(fig, use_container_width=True)