# importing necessary libraries
import streamlit as st
from src.data_loading import load_and_cache
# customizing the page
st.set_page_config(
    page_title="What Makes A Hit Song",
    page_icon=":guitar:",
    layout="wide", 
    initial_sidebar_state="expanded"
)


# describing the dashboard
st.header('The Dashboard')
st.markdown("---")
st.write("")

st.markdown("""
🎵 Take a trip down memory lane with the Billboard Hot 100!
This dashboard lets you dive into the audio profiles of chart-topping hits, year by year, and by the artists who made them.

📅 Yearly Profiles:
✨ Check out how music has changed over the years by looking at each year's unique audio profile.
🎶 Explore the energy, valence, tempo, and other audio features that show what the music was like back then.

🎤 Artist Insights:
💡 Get a deeper understanding of your favorite artists by checking out their unique audio profiles.

💖 Whether you're a music lover, a data nerd, or just curious about how the charts have changed over the years, this dashboard provides a fun and interactive way to explore what makes popular music popular.

🚀 Start your journey through music history today!      
            
""")
st.write("")
st.write("")
st.write("")
st.header('Created By')
st.markdown("---")

# name and contact info for each team member
team = {
    "Muhammad Alshakarti": "https://www.linkedin.com/in/alshakarti",
    "Wei Wang (Ella)": "https://www.linkedin.com/in/ella-wang-a393b0331/",
    "Guillermo Contreras": "https://www.linkedin.com/in/guillermocontp/",
    "Fasaam Nasrullah": "https://www.linkedin.com/in/fasaam-nasrullah-39b3a8338/",
    "Bruno Beckman": "https://www.linkedin.com/in/bruno-beckman-3a4158273/"
}

cols = st.columns(5)

# showing contact info for each team member
for (name, contact_info), col in zip(team.items(), cols):
    with col:
        st.markdown(f"**{name}**")
        st.link_button('Go to linkedin profile', contact_info)
        st.write("")

#Initializing the variables from load_and_cache
if "data_loaded" not in st.session_state:  
    variables = load_and_cache()  # Call the function once
    keys = ["audio_df", "track_df", "spotify_df", "mapping", "artists", "artist_track_", "audio_features", "trending_artists"]
    
    # Store all variables in session state dynamically
    for key, value in zip(keys, variables):
        st.session_state[key] = value

    st.session_state.data_loaded = True  # Flag to avoid reloading


