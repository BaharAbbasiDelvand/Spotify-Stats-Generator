import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

time_ranges = ['short_term', 'medium_term', 'long_term']
time_range_labels = {
    'short_term': 'Last 4 Weeks',
    'medium_term': 'Last 6 Months',
    'long_term': 'All Time'
}

def get_top_tracks(time_range):
    top_tracks = sp.current_user_top_tracks(limit=20, time_range=time_range)
    tracks_data = []
    for idx, track in enumerate(top_tracks['items']):
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        track_popularity = track['popularity']
        tracks_data.append([track_name, artist_name, track_popularity, idx + 1])
    return pd.DataFrame(tracks_data, columns=['Track', 'Artist', 'Popularity (for Spotify)', 'Rank (for user)'])

def get_top_artists(time_range):
    top_artists = sp.current_user_top_artists(limit=20, time_range=time_range)
    artists_data = []
    for idx, artist in enumerate(top_artists['items']):
        artist_name = artist['name']
        artists_data.append([artist_name, idx + 1])
    return pd.DataFrame(artists_data, columns=['Artist', 'Rank (for user)'])

for time_range in time_ranges:
    print(f"\nTop Tracks ({time_range_labels[time_range]}):")
    top_tracks_df = get_top_tracks(time_range)
    print(top_tracks_df)
    
    print(f"\nTop Artists ({time_range_labels[time_range]}):")
    top_artists_df = get_top_artists(time_range)
    print(top_artists_df)
    
    top_tracks_df.to_csv(f'top_spotify_tracks_{time_range}.csv', index=False)
    top_artists_df.to_csv(f'top_spotify_artists_{time_range}.csv', index=False)
