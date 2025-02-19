
## Introduction

This project is an extension of a team-based analysis originally conducted for my course at Hyper Island, where we explored song features to gain insights into music trends.

After that, I wanted to dive deeper into recommendation systems and realized this would be a great example. Many modern recommendation engines rely on embeddings—numerical representations of items (like movies or songs) learned by machine learning models. In this case, I leverage Spotify’s audio features as predefined embeddings, using attributes such as:

['danceability', 'energy', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'speechiness', 'key', 'mode', 'tempo', 'time_signature']

By representing songs as n-dimensional vectors, I can compute similarity scores to generate recommendations. While this approach captures mathematical similarities, the question remains: Do these recommendations align with human perception of musical similarity? I explore this in my blog, where I also discuss limitations and potential improvements to the system.

 
### Data sources

- **Billboard data**: Historical Billboard Hot 100 chart data.
- **Spotify data**: Artist details and audio features for tracks available on Spotify.
- **Timeframe**: 2000–2024, including only songs that charted on Billboard during this period.


### Analysis questions

#### Songs as vectors
- Can a song be accurately represented as a numerical vector?
- How well does cosine similarity reflect human-perceived musical similarity?
- With many features influencing similarity, can we refine the search by prioritizing certain features?


#### Artists as vectors

- If we aggregate song features per artist, does the resulting vector accurately represent their style?
- Do recommendations based only on numerical similarity produce interesting and relevant results?

### Genre data
- Spotify provides genre information at the artist level, but not for individual songs.
- Adding genre-based filtering could improve recommendation quality in future iterations.
### Requirements

- requirement.txt included

### Try It Out
This project is hosted on Streamlit, so you can explore the recommendations and visualizations without running the code locally.

https://recommendation-system-spotify-data.streamlit.app/

