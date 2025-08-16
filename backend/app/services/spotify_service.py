import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import List, Optional
from app.models import Track


class SpotifyService:
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    async def search_tracks(self, song_queries: List[str]) -> List[Track]:
        """
        Search for tracks on Spotify based on song queries
        """
        tracks = []
        
        for query in song_queries:
            try:
                # Search for the track
                results = self.sp.search(q=query, type='track', limit=1, market='US')
                
                if results['tracks']['items']:
                    track_data = results['tracks']['items'][0]
                    
                    # Get the largest image
                    image_url = None
                    if track_data['album']['images']:
                        image_url = track_data['album']['images'][0]['url']
                    
                    track = Track(
                        name=track_data['name'],
                        artist=track_data['artists'][0]['name'],
                        album=track_data['album']['name'],
                        spotify_url=track_data['external_urls']['spotify'],
                        preview_url=track_data.get('preview_url'),
                        image_url=image_url,
                        popularity=track_data.get('popularity'),
                        duration_ms=track_data.get('duration_ms')
                    )
                    
                    tracks.append(track)
                    
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        return tracks