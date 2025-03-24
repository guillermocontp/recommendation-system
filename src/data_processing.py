import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components
import random





def merge_artist_features(tracks, mapping, artists):

    artist_track = pd.merge(mapping, tracks, how='inner', on='track_id')
    artist_track_ = pd.merge(artists, artist_track, how='inner', on='artist_id')

    return artist_track_

st.cache_data()
def load_df(): 

    
    # loading data from csv files
    audio_features = pd.read_csv('data/audio_features.csv')
    tracks = pd.read_csv('data/tracks.csv')
    mapping = pd.read_csv('data/mapping.csv')
    artists = pd.read_csv('data/artists.csv')
    
    
    return  tracks, mapping, artists,  audio_features



def process_artist_data(artist_name, artist_track_, audio_features):
    """
    Process data for a given artist name to calculate charts and audio features.

    Args:
        artist_name (str): Name of the artist.
        artist_track_chart (pd.DataFrame): DataFrame with artist and track chart data.
        chart (pd.DataFrame): DataFrame with chart data.
        audio_features (pd.DataFrame): DataFrame with audio features.

    Returns:
        tuple: A tuple containing:
            - artist_charts (pd.DataFrame): DataFrame with artist chart data.
            - artist_features (pd.DataFrame): DataFrame with artist features.
            - artist_features_mean (pd.DataFrame): DataFrame with mean features for the artist.
    """

    artist_data = artist_track_[artist_track_['name_x'] == artist_name].groupby(['track_id'])
    artist_data = pd.DataFrame(artist_data)

    artist_mapped = artist_data[0].map(lambda x: x[0])
    artist_mapped = pd.DataFrame(artist_mapped)
    artist_features_ = pd.merge(artist_mapped, audio_features, left_on=0, right_on='track_id', how='inner')
    artist_features_mean = artist_features_.agg({
        'danceability': 'mean',
        'energy': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'valence': 'mean',
        'speechiness': 'mean',
        'key': 'mean',
        'mode': 'mean',
        'tempo': 'mean',
        'time_signature': 'mean',
    }).reset_index()
    artist_features_mean['name'] = artist_name

    return artist_features_mean

def process_songs(song1_name,  tracks_features):
    test = tracks_features[tracks_features['name'] == song1_name].agg({
        'danceability': 'mean',
        'energy': 'mean',
        'acousticness': 'mean',
        'instrumentalness': 'mean',
        'liveness': 'mean',
        'valence': 'mean',
        'speechiness': 'mean',
        'key': 'mean',
        'mode': 'mean',
        'tempo': 'mean',
        'time_signature': 'mean',
    }).reset_index()
    test['name'] = song1_name
    return test

def data_to_radar_chart(*tables):
    """
    Concatenate any number of DataFrames into a radar chart table.

    Args:
        *tables: One or more pandas DataFrames, each having 'name', 'index', and 0 as columns.

    Returns:
        pd.DataFrame: A single DataFrame created by concatenating all input tables.
    """
    # Convert each input table using pivot_table
    pivoted_tables = [
        table.pivot_table(index='name', columns='index', values=0, aggfunc='first').reset_index()
        for table in tables
    ]

    # Concatenate all pivoted tables
    radar_table = pd.concat(pivoted_tables, ignore_index=True)

    return radar_table







def get_artist_features(artists_df, artist_track_, audio_features):
    """
    Process features for all artists in one operation
    Inputs: A dataframe of artists, a dataframe of artist and its tracks, and a dataframe of audio features
    Outputs: A dataframe of mean audio features for each artist
    """
    # Get all relevant tracks
    artist_tracks = artist_track_[artist_track_['name_x'].isin(artists_df['name'])]
    
    # Merge with audio features
    features = pd.merge(artist_tracks[['name_x', 'track_id']], 
                       audio_features, 
                       on='track_id', 
                       how='inner')
    
    # Calculate means for each artist
    feature_columns = ['danceability', 'energy', 'acousticness', 'instrumentalness',
                      'liveness', 'valence', 'speechiness', 'key', 'mode', 
                      'tempo', 'time_signature']
    
    radar_table = features.groupby('name_x')[feature_columns].mean().reset_index()
    radar_table = radar_table.rename(columns={'name_x': 'name'})
    
    return radar_table

def get_similar_artists(artist_name, vectors, artists_df, n=20):
    """
    Find n most similar artists and return their vectors for visualization
    
    Args:
        artist_name (str): Name of the artist to find similarities for
        vectors (np.array): Normalized feature vectors
        artists_df (pd.DataFrame): DataFrame containing artist names
        n (int): Number of similar artists to return (default 20)
    
    Returns:
        tuple or str: Either (similar_vectors, similar_artists_df, similarity_scores) or error message
    """
    try:
        # First ensure vectors and artists_df are aligned
        if len(vectors) != len(artists_df):
            return f"Mismatch between vectors ({len(vectors)}) and artists ({len(artists_df)})"
            
        # Check if artist exists in DataFrame
        if artist_name not in artists_df['name'].values:
            return f"Artist '{artist_name}' not found in database"
            
        # Get artist index and vector
        artist_idx = artists_df[artists_df['name'] == artist_name].index[0]
        
        # Verify index is within bounds
        if artist_idx >= len(vectors):
            return f"Artist index {artist_idx} out of bounds for vectors length {len(vectors)}"
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(vectors)
        
        # Get similarity scores for input artist
        artist_similarities = similarity_matrix[artist_idx]
        
        # Get indices of all artists sorted by similarity
        sorted_indices = np.argsort(-artist_similarities)
        
        # Filter out the original artist and duplicates
        filtered_indices = []
        seen_names = set()
        
        # Add indices while filtering duplicates
        for idx in sorted_indices:
            name = artists_df.iloc[idx]['name']
            if name != artist_name and name not in seen_names:
                filtered_indices.append(idx)
                seen_names.add(name)
            
            # Break if we have enough unique artists
            if len(filtered_indices) >= n:
                break
                
        # Convert to numpy array and take first n
        filtered_indices = np.array(filtered_indices[:n])
        
        # Get vectors and names for similar artists
        similar_vectors = vectors[filtered_indices]
        similar_artists = artists_df.iloc[filtered_indices]
        similarity_scores = artist_similarities[filtered_indices]
        
        return similar_vectors, similar_artists, similarity_scores
        
    except Exception as e:
        return f"Error processing artist '{artist_name}': {str(e)}"
    

def vectorize_artist_features(artist_features):
    """
    Vectorize artist features for similarity calculation.
    
    Args:
        artist_features (pd.DataFrame): DataFrame with artist features
        
    Returns:
        tuple: (normalized vectors, cleaned DataFrame)
            - normalized vectors: numpy array of normalized features
            - cleaned DataFrame: DataFrame with same indices as vectors
    """
    # Define features to use
    features_to_normalize = ['danceability', 'energy', 'acousticness', 'instrumentalness',
                           'liveness', 'valence', 'speechiness', 'key', 'mode', 
                           'tempo', 'time_signature']
    
    # Check for missing values
    missing_mask = artist_features[features_to_normalize].isna().any(axis=1)
    if missing_mask.any():
        print(f"Removing {missing_mask.sum()} rows with missing values")
        artist_features = artist_features[~missing_mask].copy()
    
    # Normalize features
    scaler = MinMaxScaler()
    vectors_normalized = scaler.fit_transform(artist_features[features_to_normalize])
    
    # Create clean DataFrame with same index as vectors
    cleaned_df = artist_features.reset_index(drop=True)
    
    return vectors_normalized, cleaned_df

def apply_feature_weights(vectors, weights=None):
    """
    Apply weights to feature vectors
    
    Args:
        vectors (pd.DataFrame): Feature vectors
        weights (dict): Dictionary of feature weights, default None
        possible features: 'danceability', 'energy', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 
        'speechiness', 'key', 'mode', 'tempo','time_signature'
        
    Returns:
        pd.DataFrame: Weighted feature vectors
    """
    # Define available features
    available_features = ['danceability', 'energy', 'acousticness', 
                         'instrumentalness', 'liveness', 'valence', 
                         'speechiness', 'key', 'mode', 'tempo', 
                         'time_signature']
    
    # Convert DataFrame to numpy array if needed
    if isinstance(vectors, pd.DataFrame):
        vectors = vectors[available_features].to_numpy()
    
    # Use default weights if none provided
    if weights is None:
        return vectors
    
    # Validate weights
    invalid_features = [f for f in weights.keys() if f not in available_features]
    if invalid_features:
        raise ValueError(f"Invalid features in weights: {invalid_features}")
    
    # Create weight array in same order as features
    weight_array = np.ones(len(available_features))
    for i, feature in enumerate(available_features):
        if feature in weights:
            weight_array[i] = weights[feature]
    
    # Apply weights
    weighted_vectors = vectors * weight_array
    
    return weighted_vectors


def get_artist_sample(vectors, artists_df, sample_size=30):
    """Sample random subset of artists and their vectors
        inputs: A dataframe of artist vectors and a dataframe of artist names
        outputs: A sample of artist vectors and names
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Get random indices
    sample_indices = np.random.choice(
        len(vectors), 
        size=min(sample_size, len(vectors)), 
        replace=False
    )
    
    # Sample both datasets using same indices
    vectors_sample = vectors.iloc[sample_indices]
    artists_sample = artists_df.iloc[sample_indices]
    
    return vectors_sample, artists_sample

def reset_weights_callback():
    """Simple callback to reset all weight-related state"""
    # Reset weights dictionary
    st.session_state.weights = {}
    
    # Clear all weight-specific states
    for key in list(st.session_state.keys()):
        if key.startswith('weight_'):
            del st.session_state[key]

    # Reset vectors to original state (no weights applied)
    st.session_state.vectors = st.session_state.get('original_vectors', None)


    # Add this at the top of your home.py file



def inject_ga_with_variant():
    GA_MEASUREMENT_ID = "G-D428JCS6W2"  # Your measurement ID
    
    # Use .get() method with default values to prevent KeyError
    variant = st.session_state.get("ab_variant", "not_set")
    variant_features = st.session_state.get("variant_features", "not_set")
    
    # Debug message visible in browser console
    debug_script = """
    <script>
      console.log('GA Debugging: Script loaded');
      console.log('GA ID: G-D428JCS6W2');
    </script>
    """
    
    # Complete HTML document structure for GA script
    GA_SCRIPT = f"""
    <head>
      <!-- Google tag (gtag.js) -->
      <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
      <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}};
        gtag('js', new Date());
        gtag('config', '{GA_MEASUREMENT_ID}', {{
          'ab_variant': '{variant}',
          'variant_features': '{variant_features}'
        }});
        console.log('GA Debugging: gtag configured');
      </script>
    </head>
    """
    
    # Inject both scripts
    components.html(debug_script + GA_SCRIPT, height=0)
    
    # Add a visible indicator during development
    st.sidebar.caption("📊 Analytics enabled")

    # A/B testing setup
def setup_ab_testing():
    """Initialize A/B testing variants if not already assigned"""
    if "ab_variant" not in st.session_state:
        # Randomly assign user to variant A or B (50/50 split)
        variant = random.choice(["A", "B"])
        st.session_state.ab_variant = variant
        
        # Track assignment event
        if variant == "A":
            st.session_state.variant_features = "original"
        else:
            st.session_state.variant_features = "enhanced"
            
        # Log the variant assignment (for debugging)
        print(f"User assigned to variant: {variant}")


def track_page_navigation(page_name):
    """
    Tracks page navigation events in Google Analytics
    Args:
        page_name: Name of the current page
    """
    GA_MEASUREMENT_ID = "G-D428JCS6W2"  # Your Google Analytics ID
    
    # Get current variant info
    variant = st.session_state.get("ab_variant", "not_set")
    variant_features = st.session_state.get("variant_features", "not_set")
    
    # Create tracking script for page view
    tracking_script = f"""
    <script>
        // Send page view event to Google Analytics
        gtag('event', 'page_view', {{
            'page_title': '{page_name}',
            'page_location': window.location.href,
            'ab_variant': '{variant}',
            'variant_features': '{variant_features}'
        }});
        
        console.log('Tracked page view: {page_name}');
    </script>
    """
    components.html(tracking_script, height=0)


# Add this to data_processing.py
def track_button_clicks():
    """
    Track clicks on common buttons by their text content
    """
    tracking_code = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add a small delay to ensure buttons are rendered
        setTimeout(function() {
            // Find all buttons on the page
            document.querySelectorAll('button').forEach(function(button) {
                // Check if we've already attached a listener
                if (!button.hasAttribute('data-tracked')) {
                    // Mark as tracked to avoid duplicate events
                    button.setAttribute('data-tracked', 'true');
                    
                    // Add click listener
                    button.addEventListener('click', function() {
                        // Get button text as identifier
                        var buttonText = button.innerText.trim();
                        
                        // Track the click event
                        if (typeof gtag === 'function') {
                            gtag('event', 'button_click', {
                                'button_text': buttonText,
                                'page_path': window.location.pathname,
                                'ab_variant': sessionStorage.getItem('ab_variant') || 'not_set'
                            });
                            console.log('Tracked click on button: ' + buttonText);
                        }
                    });
                }
            });
        }, 1000); // 1 second delay
    });
    </script>
    """
    components.html(tracking_code, height=0)