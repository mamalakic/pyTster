import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config


class SpotifyClient:
    def __init__(self):
        if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
            raise ValueError(
                "Spotify credentials not found. Set SPOTIFY_CLIENT_ID "
                "and SPOTIFY_CLIENT_SECRET in .env file"
            )
        
        auth = SpotifyClientCredentials(
            client_id=config.SPOTIFY_CLIENT_ID,
            client_secret=config.SPOTIFY_CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(auth_manager=auth)
    
    def extract_playlist_id(self, url):
        if 'spotify.com/playlist/' in url:
            return url.split('playlist/')[-1].split('?')[0]
        return url
    
    def get_playlist_songs(self, playlist_url, num_songs=None):
        num_songs = num_songs or config.SONGS_PER_PLAYLIST
        playlist_id = self.extract_playlist_id(playlist_url)
        
        songs = []
        offset = 0
        
        while len(songs) < num_songs:
            results = self.sp.playlist_tracks(
                playlist_id,
                offset=offset,
                limit=min(100, num_songs - len(songs))
            )
            
            if not results['items']:
                break
            
            for item in results['items']:
                if not item['track']:
                    continue
                
                track = item['track']
                popularity = track.get('popularity', 0)
                
                if popularity < config.MIN_TRACK_POPULARITY:
                    continue
                
                artists = ', '.join([a['name'] for a in track['artists']])
                release_date = track['album']['release_date']
                year = release_date.split('-')[0] if release_date else 'Unknown'
                
                songs.append({
                    'title': track['name'],
                    'artists': artists,
                    'year': year,
                    'url': track['external_urls']['spotify'],
                    'popularity': popularity,
                    'playlist_owner': None
                })
                
                if len(songs) >= num_songs:
                    break
            
            offset += len(results['items'])
            if not results['next']:
                break
        
        return songs[:num_songs]
    
    def get_multiple_playlists(self, playlist_urls, songs_per_playlist=None):
        all_songs = []
        
        for i, url in enumerate(playlist_urls):
            print(f"Fetching playlist {i+1}/{len(playlist_urls)}...")
            songs = self.get_playlist_songs(url, songs_per_playlist)
            
            for song in songs:
                song['playlist_owner'] = f"Player {i+1}"
            
            all_songs.extend(songs)
            print(f"  Fetched {len(songs)} songs")
        
        return all_songs
