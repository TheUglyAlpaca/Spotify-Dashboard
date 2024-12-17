import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Spotify credentials from environment variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000'  # Adjust port if needed

# Spotify API Authorization
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read user-library-read playlist-read-private',
    )
)

# Streamlit App Setup
st.set_page_config(page_title='Spotify Song Analysis', page_icon=':musical_note:')
st.title('🎶 Your Top 20 Spotify Wrapped 🎶')
st.markdown('Welcome to your personalized **Spotify Song Insights**! Here you can explore your top 20 songs over the past few weeks and your all-time favorites.')

# Fetch user's top 20 songs in the short term (last 4 weeks)
top_tracks_short_term = sp.current_user_top_tracks(limit=20, time_range='short_term')  # Last 4 weeks

# Extract track names and artists for short term
track_names_short_term = [track['name'] for track in top_tracks_short_term['items']]
artists_short_term = [', '.join([artist['name'] for artist in track['artists']]) for track in top_tracks_short_term['items']]

# Create DataFrame for short-term top tracks (without popularity)
df_short_term = pd.DataFrame({
    'Track Name': track_names_short_term,
    'Artists': artists_short_term
})

# Fetch user's top 20 songs in the long term (all-time)
top_tracks_long_term = sp.current_user_top_tracks(limit=20, time_range='long_term')  # All-time

# Extract track names and artists for long term
track_names_long_term = [track['name'] for track in top_tracks_long_term['items']]
artists_long_term = [', '.join([artist['name'] for artist in track['artists']]) for track in top_tracks_long_term['items']]

# Create DataFrame for long-term top tracks (without popularity)
df_long_term = pd.DataFrame({
    'Track Name': track_names_long_term,
    'Artists': artists_long_term
})

# Streamlit Layout: Display tables side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader('Recent Top 20')
    st.write(df_short_term)

with col2:
    st.subheader('All Time Top 20')
    st.write(df_long_term)

# Add a neat table style
st.markdown("""
<style>
    .streamlit-expanderHeader {
        font-size: 24px;
        color: #1DB954;
    }
    .css-17eq0y5 {
        font-size: 18px;
        text-align: center;
        color: #333;
    }
    .css-1y2sjz0 {
        font-size: 18px;
        font-weight: 600;
    }
    .css-1v3fvcr {
        font-size: 16px;
    }
    .css-1f9m1f5 {
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# Add clickable links for both short-term and long-term songs
st.write("---")
st.markdown("Want to listen to these songs? Click the names below to open them on Spotify!")

# Short-term top tracks with links
st.markdown("**🎵 Your Top Songs (Last 4 Weeks):**")
for index, row in df_short_term.iterrows():
    track_url = f"https://open.spotify.com/track/{top_tracks_short_term['items'][index]['id']}"
    st.markdown(f"[{row['Track Name']}]({track_url}) by {row['Artists']}")

# Long-term top tracks with links
st.write("---")
st.markdown("**🎶 Your Top Songs (All Time):**")
for index, row in df_long_term.iterrows():
    track_url = f"https://open.spotify.com/track/{top_tracks_long_term['items'][index]['id']}"
    st.markdown(f"[{row['Track Name']}]({track_url}) by {row['Artists']}")
