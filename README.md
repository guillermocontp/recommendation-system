
## Introduction

This system is derived from a project done by a team for a Hyper Island class. We analyzed the features of the songs.

After that I wanted to explore the recommendations systems more in depth and I thought this was a cool example. In many of those engines, you have embeddings of the items you want to recommend (like movies) and those are done by a ML model. In this case, I can use the features of the songs: ['danceability', 'energy', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'speechiness', 'key', 'mode', 
                'tempo', 'time_signature']
to group the songs in a n-dimensional vector space. Then I can use similarity to give recommendations. 
This approach is further discussed in my blog, where I also talk about the limitations and possible further steps.

 
### Data sources

- **Billboard data**: Historical chart data from the Billboard Hot 100.
- **Spotify data**: Artist information and audio features for tracks available on Spotify.
- The data is from 2000 to 2024 and is only about songs that made it to the Billboard charts during that period.

### Analysis questions

#### Songs as vectors
- Is it possible to approximate a song as a vector?
- How accurate can two vectors represent songs that a human will think as alike?
- There are many features and some are more important than others, is it possible to refine this search?


#### Artists as vectors

- If you group the songs per artist, do you get an accurate representation of what an artist is?
- With this criteria, how interesting are the recommendations, based only on numeric values?

### Genre data
- Spotify does have genre data, but only related to artists. As an improvement this data could be added to further filter the recommendations.

### Requirements

- requirement.txt included

### This repo is hosted in Streamlit if you only want to see it 