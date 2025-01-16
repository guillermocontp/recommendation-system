# importing necessary libraries
import streamlit as st
import pandas as pd 
import plotly.express as px

# importing project functions

from src.visualization import (
    plot_yearly_features,
    plot_single_feature, 
    plot_feature_averages,
    plot_year_comparison,
    style_chart,
    display_metrics
)

from src.filter import (
    filter_data_by_years,
    prepare_yearly_feature_data,
    prepare_comparison_data,
    create_sidebar_filters,
    initialize_features_and_averages,
    filter_year_data
)

# loading pre-processed data 
audio_df = pd.read_csv('data/audio_data.csv')
track_df = pd.read_csv('data/track_data.csv')
spotify_df = pd.read_csv('data/spotify_data.csv')

# customizing the page
st.set_page_config(
    page_title="What Makes A Hit Song",
    page_icon=":guitar:",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# defining features list for visualization and average track data for track features
features, avg_data = initialize_features_and_averages(track_df)


# adding sidebar titel and buttons
with st.sidebar:
    st.title("🎸 What Makes A Hit Song")
    
    # creating button for analysis type selection 
    analysis_type = st.radio(
        'Choose Analysis Type',
        ['Timeline Analysis', 'Single Year Analysis', 'Year Comparison'],
        key = "analysis_type"
    )

# creating two columns and setting margins
col1, col2 = st.columns([4,1])

# first column of page
with col1:
    # adding header
    st.header('Song Characteristics')
    st.markdown("---")
    
    # visualizing average audio features year by year
    if analysis_type == 'Timeline Analysis':
        
        # define start, end year and feature view:
        start_year, end_year, feature_view = create_sidebar_filters(audio_df)
            
        # allow users to select year range using selectbox
        filtered_audio_df, filtered_track_df, avg_filtered_track_df = filter_data_by_years(audio_df, track_df, start_year, end_year)
        
        # if user selects all features 
        if feature_view == 'All characteristics':
            
            st.subheader('All Song Characteristics Over Time')
            
            # plotting all features
            fig = plot_yearly_features(filtered_audio_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # display track metrics
            display_metrics(avg_filtered_track_df, avg_data)

        # if user selects single feature
        else:
            # adding feature type selection option
            selected_feature = st.sidebar.selectbox(
                'Select Characteristics',
                features,
                key = 'single_feature'
            )
            
            # updating header 
            st.subheader(f'{selected_feature} Over Time')
            
            # plotting single feature
            fig = plot_single_feature(filtered_audio_df, selected_feature)
            st.plotly_chart(fig, use_container_width=True)
            
            # display track metrics
            display_metrics(avg_filtered_track_df, avg_data)

            
    # if user selects single year analysis
    elif analysis_type == 'Single Year Analysis':
    
        # creating select box for year
        year = st.sidebar.selectbox('Select Year', sorted(audio_df['year'].unique(), reverse=True))
        
        # updating header 
        st.subheader(f'Average Song Characteristics during {year}')
        
        # filtering data for selected year
        melted_audio_df = prepare_yearly_feature_data(audio_df, year, features)
        
        # plot data for selected year
        fig = plot_feature_averages(melted_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # getting data for selected year 
        selected_year_track_data = track_df[track_df['year'] == year]
        
        # display track metrics
        display_metrics(selected_year_track_data, avg_data)

    # if user selects year comparison
    else:
    
        # creating select box for each year
        year1 = st.sidebar.selectbox('Select First Year', sorted(audio_df['year'].unique(), reverse=True), key='year1')
        year2 = st.sidebar.selectbox('Select Second Year', sorted(audio_df['year'].unique(), reverse=True), key='year2', index=1)
        
        # updating header 
        st.subheader(f'Average Song Characteristics during {year1} vs {year2}')
        
        # filtering data for each year
        audio_df_year1, audio_df_year2, track_df_year1, track_df_year2 = filter_year_data(
            audio_df, track_df, year1, year2, features
        )
       
        comparison_audio_df = prepare_comparison_data(audio_df, year1, year2, features)
        
        # showing comparison chart: 
        fig = plot_year_comparison(comparison_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # getting data for selected year 
        track_df_year1 = track_df[audio_df['year'] == year1]
        track_df_year2 = track_df[audio_df['year'] == year2]
        
        st.subheader(f'{year1}')
        
        # display track metrics
        display_metrics(track_df_year1, avg_data)
        
        st.subheader(f'{year2}')
        
        # display track metrics
        display_metrics(track_df_year2, avg_data)
        
        # customizing the chart design 
        fig = style_chart(fig)
    
    # Add space and divider
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # adding feature descriptions
    st.markdown('### Audio Characteristics Descriptions')
    
    # description of each feature
    feature_descriptions = {
        "danceability": "How suitable a track is for dancing based on tempo, rhythm stability, beat strength, and overall regularity.",
        "energy": "Represents the intensity and activity level of the track.",
        "acousticness": "A confidence measure of whether the track is acoustic.",
        "instrumentalness": "Predicts whether a track contains no vocals.",
        "liveness": "Detects the presence of an audience in the recording.",
        "valence": "Describes the musical positiveness conveyed by a track."
    }
    
    # creating printing feature descriptions
    for feature, description in feature_descriptions.items():
        st.write(f"**{feature.title()}:** {description}")

#with col2: