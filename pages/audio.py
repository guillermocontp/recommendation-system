# importing necessary libraries
import streamlit as st
import os
from dotenv import load_dotenv
from src.data_loading import audio_df, track_df, spotify_songs, mapping, artists, artist_track_, audio_features, trending_artists


# importing necessary functions from src    
from src.visualization import (
    plot_yearly_features,
    plot_single_feature, 
    plot_year_comparison,
    style_chart,
    display_metrics,
)
from src.filter import (
    filter_data_by_years,
    prepare_comparison_data,
    create_sidebar_filters,
    initialize_features_and_averages,
    filter_year_data, 
    filter_spotify_by_year,
    prepare_yearly_comparison_data
)
from src.spotify_widget import (
    get_spotify_components,
    show_spotify_components,
    get_token,
    fetch_and_parse_spotify_data,
    filter_spotify_by_year,
    filter_spotify_by_single_year,
    filter_spotify_for_comparison,
    filter_spotify_by_year_and_feature,
    show_spotify_components_min_max,
)
from home import load_and_cache

# loading Spotify credentials (for API) from .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
token = get_token(client_id, client_secret)

# defining features list for visualization and average track data for track features
features, avg_data = initialize_features_and_averages(track_df, audio_df)

# creating sidebar filters
with st.sidebar:
    st.title("Filters")
    
    # selectbox for view selection
    analysis_type = st.sidebar.selectbox(
        'Select View',
        ['Trends', 'Specific', 'Comparison'],
        key = "analysis_type"
    )

# creating two columns and setting margins
col1, spacer, col2 = st.columns([3.5, 0.5, 1])

# visualizing audio features
with col1:
    st.header('Yearly Audio Profile')
    st.markdown("---")
    
    # if user selects trends
    if analysis_type == 'Trends':
        
        # create filter selectbox for year range
        start_year, end_year, feature_view = create_sidebar_filters(audio_df)
            
        # defining year range
        filtered_audio_df, filtered_track_df, avg_filtered_track_df = filter_data_by_years(audio_df, track_df, start_year, end_year)
        
        # if user selects all metrics 
        if feature_view == 'All metrics':
            
            st.subheader('Audio Profile Trends')
            
            # visualizing and showing all features
            fig = plot_yearly_features(filtered_audio_df)
            st.plotly_chart(fig, use_container_width=True)
            display_metrics(avg_filtered_track_df, avg_data)

        # if user selects single metric
        else:
            # creating selectbox 
            selected_feature = st.sidebar.selectbox(
                'Select metric',
                features,
                key = 'single_feature'
            )
            
            st.subheader(f'{selected_feature} Over Time')
            
            # visualizing and showing selected features
            fig = plot_single_feature(filtered_audio_df, selected_feature)
            st.plotly_chart(fig, use_container_width=True)
            display_metrics(avg_filtered_track_df, avg_data)
        
    # if user selects specific
    elif analysis_type == 'Specific':
        
        # creating select box for year
        year = st.sidebar.selectbox('Select Year', sorted(audio_df['year'].unique(), reverse=True))
        st.subheader(f'{year} Audio Profile')
        
        # visualizing and showing selected year
        melted_audio_df = prepare_yearly_comparison_data(audio_df, year, features)
        fig = plot_year_comparison(melted_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        selected_year_track_data = track_df[track_df['year'] == year]
        display_metrics(selected_year_track_data, avg_data)

    # if user selects comparison
    else:
    
        # creating select box for each year
        year1 = st.sidebar.selectbox('Select First Year', sorted(audio_df['year'].unique(), reverse=True), key='year1')
        year2 = st.sidebar.selectbox('Select Second Year', sorted(audio_df['year'].unique(), reverse=True), key='year2', index=1)
        st.subheader(f'{year1} vs {year2} Audio Profile')
        
        # filtering data for each year
        audio_df_year1, audio_df_year2, track_df_year1, track_df_year2 = filter_year_data(
            audio_df, track_df, year1, year2, features
        )
        comparison_audio_df = prepare_comparison_data(audio_df, year1, year2, features)
        
        # visualizing and showing selected years
        fig = plot_year_comparison(comparison_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        track_df_year1 = track_df[audio_df['year'] == year1]
        track_df_year2 = track_df[audio_df['year'] == year2]
        st.subheader(f'{year1}')
        display_metrics(track_df_year1, avg_data)
        st.write("")
        st.subheader(f'{year2}')
        display_metrics(track_df_year2, avg_data)
        st.write("")
        fig = style_chart(fig)
        
    # Song Characteristics Descriptions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('### Audio Characteristics Descriptions')
    st.markdown("---")
    st.write("")
    
    # description of each feature
    feature_descriptions = {
        "Danceability": "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.",
        "Energy": "Energy represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
        "Acousticness": "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
        "Instrumentalness": 'Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.',
        "Speechiness": "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
        "Liveness": "Liveness detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
        "Valence": "A describes the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
        "Tempo": "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
        "Loudness": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.",
        "Duration": "The duration of the track in minutes."
    }
    
    with st.container(height=200):
        for feature, description in feature_descriptions.items():

            with st.expander(feature):
                st.write(description)

# fetch and snow song data
with col2:
    st.header('Examples')
    st.markdown("---")
    st.write("")

    # if user selects trends 
    if analysis_type == 'Trends':
        
        # if user selects all features 
        if feature_view == 'All metrics':
            
            # filter songs by year range
            spotify_recommendations = filter_spotify_by_year(start_year, end_year, spotify_songs)
            
            # fetching data and visualizing songs
            parsed_recommendations = fetch_and_parse_spotify_data(spotify_recommendations, token, client_id, client_secret)
            song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3 = get_spotify_components(parsed_recommendations)
            show_songs = show_spotify_components(song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3) 
        
        # if user selects specific features 
        else:
            # filter songs by year range and selected feature
            max_song, min_song = filter_spotify_by_year_and_feature(start_year, end_year, spotify_songs, selected_feature)
            
            # fetching data and visualizing songs
            max_song_df = fetch_and_parse_spotify_data(max_song, token, client_id, client_secret)
            min_song_df = fetch_and_parse_spotify_data(min_song, token, client_id, client_secret)
            show_spotify_components_min_max(max_song_df, min_song_df, selected_feature)
                   
    # if user selects single year analysis
    elif analysis_type == 'Specific':
        
        # filter songs by year
        spotify_recommendations =  filter_spotify_by_single_year(year, spotify_songs)
        
        # fetching data and visualizing songs
        parsed_recommendations = fetch_and_parse_spotify_data(spotify_recommendations, token, client_id, client_secret)
        song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3 = get_spotify_components(parsed_recommendations)
        show_songs = show_spotify_components(song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3) 
            
    # if user selects year comparison
    else:
        # filter songs by years 
        year1_spotify_recommendations, year2_spotify_recommendations = filter_spotify_for_comparison(year1, year2, spotify_songs)
        
        # fetching data and visualizing songs for year 1 and 2
        # year 1 songs 
        st.subheader(f'{year1}')
        year1_parsed_recommendations = fetch_and_parse_spotify_data(year1_spotify_recommendations, token, client_id, client_secret)
        song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3 = get_spotify_components(year1_parsed_recommendations)
        year1_show_songs = show_spotify_components(song1, song2, song3, artist1, artist2, artist3, url1, url2, url3, cover1, cover2, cover3) 
        
        # year 2 songs 
        st.subheader(f'{year2}')
        year2_parsed_recommendations = fetch_and_parse_spotify_data(year2_spotify_recommendations, token, client_id, client_secret)
        song4, song5, song6, artist4, artist5, artist6, url4, url5, url6, cover4, cover5, cover6 = get_spotify_components(year2_parsed_recommendations)
        year1_show_songs = show_spotify_components(song4, song5, song6, artist4, artist5, artist6, url4, url5, url6, cover4, cover5, cover6) 