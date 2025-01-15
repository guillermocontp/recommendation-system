# importing necessary libraries
import streamlit as st
import pandas as pd 
import plotly.express as px

from src.visualization import plot_yearly_features, plot_single_feature, plot_feature_averages , plot_year_comparison, style_chart
from src.filter import filter_data_by_years, prepare_yearly_feature_data, prepare_comparison_data

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

# defining features list for visualization
features = ['danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'valence']

# defining average data for track features
avg_data = track_df.mean()


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
    st.header('Audio Features')
    st.markdown("---")
    
    # visualizing average audio features year by year
    if analysis_type == 'Timeline Analysis':
        
        # allow users to select year range using selectbox
        available_years = sorted(audio_df['year'].unique().tolist())
        
        start_year = st.sidebar.selectbox(
            "Start Year",
            options=available_years,
            index=0,  # Default to first year
            key='start_year'
        )

        end_year = st.sidebar.selectbox(
            "End Year",
            options=available_years,
            index=len(available_years)-1,  # Default to last year
            key='end_year'
        )      
    
        # adding feature selection option
        feature_view = st.sidebar.selectbox(
            'Select View',
            ['All Features', 'Single Feature'],
            key = 'feature_view'
        )
        
        # filtering data on selected years 
        filtered_audio_df, filtered_track_df, avg_filtered_track_df = filter_data_by_years(audio_df, track_df, start_year, end_year)
        
        # if user selects all features 
        if feature_view == 'All Features':
            
            st.subheader('All Song Features Over Time')
            
            # plotting all features
            fig = plot_yearly_features(filtered_audio_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # creating three columns for metrics
            m1, m2, m3 = st.columns(3)
            
            # showing metrics for tempo, loudness, and duration + deltas
            with m1:
                tempo_delta = round(avg_filtered_track_df['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
                st.metric(
                    label="Average Tempo",
                    value=f"{round(avg_filtered_track_df['Tempo (BPM)'].mean())} BPM",
                    delta=f"{tempo_delta} BPM"
                )
            
            with m2:
                loudness_delta = round(avg_filtered_track_df['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
                st.metric(
                    label="Average Loudness",
                    value=f"{round(avg_filtered_track_df['Loudness (dB)'].mean())} dB",
                    delta=f"{loudness_delta} dB"
                )
            
            with m3:
                duration_delta = round(avg_filtered_track_df['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
                st.metric(
                    label="Average Duration",
                    value=f"{round(avg_filtered_track_df['Duration (min)'].mean(), 2)} min",
                    delta=f"{duration_delta} min"
                )

        # if user selects single feature
        else:
            # adding feature type selection option
            selected_feature = st.sidebar.selectbox(
                'Select Feature',
                features,
                key = 'single_feature'
            )
            
            # updating header 
            st.subheader(f'{selected_feature} Over Time')
            
            # plotting single feature
            fig = plot_single_feature(filtered_audio_df, selected_feature)
            st.plotly_chart(fig, use_container_width=True)
            
            # creating three columns for metrics
            m1, m2, m3 = st.columns(3)
            
            # showing metrics for tempo, loudness, and duration + deltas
            with m1:
                tempo_delta = round(avg_filtered_track_df['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
                st.metric(
                    label="Average Tempo",
                    value=f"{round(avg_filtered_track_df['Tempo (BPM)'].mean())} BPM",
                    delta=f"{tempo_delta} BPM"
                )
            
            with m2:
                loudness_delta = round(avg_filtered_track_df['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
                st.metric(
                    label="Average Loudness",
                    value=f"{round(avg_filtered_track_df['Loudness (dB)'].mean())} dB",
                    delta=f"{loudness_delta} dB"
                )
            
            with m3:
                duration_delta = round(avg_filtered_track_df['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
                st.metric(
                    label="Average Duration",
                    value=f"{round(avg_filtered_track_df['Duration (min)'].mean(), 2)} min",
                    delta=f"{duration_delta} min"
                )
            
    # if user selects single year analysis
    elif analysis_type == 'Single Year Analysis':
    
        # creating select box for year
        year = st.sidebar.selectbox('Select Year', sorted(audio_df['year'].unique(), reverse=True))
        
        # updating header 
        st.subheader(f'Average Song Features in {year}')
        
        # filtering data for selected year
        melted_audio_df = prepare_yearly_feature_data(audio_df, year, features)
        
        # plot data for selected year
        fig = plot_feature_averages(melted_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        
         # creating three columns for metrics
        m1, m2, m3 = st.columns(3)
        
        # getting data for selected year 
        selected_year_track_data = track_df[track_df['year'] == year]
        
        # showing metrics for tempo, loudness, and duration + deltas
        with m1:
            tempo_delta = round(selected_year_track_data['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
            st.metric(
                label="Average Tempo",
                value=f"{round(selected_year_track_data['Tempo (BPM)'].mean())} BPM",
                delta=f"{tempo_delta} BPM"
            )
        
        with m2:
            loudness_delta = round(selected_year_track_data['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
            st.metric(
                label="Average Loudness",
                value=f"{round(selected_year_track_data['Loudness (dB)'].mean())} dB",
                delta=f"{loudness_delta} dB"
            )
        
        with m3:
            duration_delta = round(selected_year_track_data['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
            st.metric(
                label="Average Duration",
                value=f"{round(selected_year_track_data['Duration (min)'].mean(), 2)} min",
                delta=f"{duration_delta} min"
            )

    # if user selects year comparison
    else:
    
        # creating select box for each year
        year1 = st.sidebar.selectbox('Select First Year', sorted(audio_df['year'].unique(), reverse=True), key='year1')
        year2 = st.sidebar.selectbox('Select Second Year', sorted(audio_df['year'].unique(), reverse=True), key='year2', index=1)
        
        # updating header 
        st.subheader(f'Average Song Feature Comparison: {year1} vs {year2}')
        
        # filtering data for each year
        audio_df_year1 = audio_df[audio_df['year'] == year1][features].mean()
        audio_df_year2 = audio_df[audio_df['year'] == year2][features].mean()
       
        comparison_audio_df = prepare_comparison_data(audio_df, year1, year2, features)
        
        # showing comparison chart: 
        fig = plot_year_comparison(comparison_audio_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(f'{year1}')
        
        # creating three columns for metrics
        m1, m2, m3 = st.columns(3)
        
        # getting data for selected year 
        track_df_year1 = track_df[audio_df['year'] == year1]
        track_df_year2 = track_df[audio_df['year'] == year2]
    
        # showing year 1 metrics for tempo, loudness, and duration + deltas
        with m1:
            tempo_delta = round(track_df_year1['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
            st.metric(
                label="Average Tempo",
                value=f"{round(track_df_year1['Tempo (BPM)'].mean())} BPM",
                delta=f"{tempo_delta} BPM"
            )
        
        with m2:
            loudness_delta = round(track_df_year1['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
            st.metric(
                label="Average Loudness",
                value=f"{round(track_df_year1['Loudness (dB)'].mean())} dB",
                delta=f"{loudness_delta} dB"
            )
        
        with m3:
            duration_delta = round(track_df_year1['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
            st.metric(
                label="Average Duration",
                value=f"{round(track_df_year1['Duration (min)'].mean(), 2)} min",
                delta=f"{duration_delta} min"
            )
        
        st.subheader(f'{year2}')
        
        m4, m5, m6 = st.columns(3)
        
        # showing year 2 metrics for tempo, loudness, and duration + deltas
        with m4:
            tempo_delta = round(track_df_year2['Tempo (BPM)'].mean() - avg_data['Tempo (BPM)'].mean(), 1)
            st.metric(
                label="Average Tempo",
                value=f"{round(track_df_year2['Tempo (BPM)'].mean())} BPM",
                delta=f"{tempo_delta} BPM"
            )
        
        with m5:
            loudness_delta = round(track_df_year2['Loudness (dB)'].mean() - avg_data['Loudness (dB)'].mean(), 1)
            st.metric(
                label="Average Loudness",
                value=f"{round(track_df_year2['Loudness (dB)'].mean())} dB",
                delta=f"{loudness_delta} dB"
            )
        
        with m6:
            duration_delta = round(track_df_year2['Duration (min)'].mean() - avg_data['Duration (min)'].mean(), 2)
            st.metric(
                label="Average Duration",
                value=f"{round(track_df_year2['Duration (min)'].mean(), 2)} min",
                delta=f"{duration_delta} min"
            )  

        # customizing the chart design 
        fig = style_chart(fig)
    
    # Add space and divider
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # adding feature descriptions
    st.markdown('### Audio Feature Descriptions')
    
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