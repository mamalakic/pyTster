"""Fetch and filter user's liked songs by popularity."""


"""
Standalone script to filter your Spotify liked songs by popularity.

Usage:
    python filter_liked_songs.py                           # Print to console (popularity >= 80)
    python filter_liked_songs.py --output liked.csv        # Save to CSV
    python filter_liked_songs.py --popularity 90 --output liked.csv  # Custom threshold

Note: Popularity is Spotify's 0-100 metric roughly correlated with streams.
      ~80+ = very popular tracks (>200M streams equivalent)
"""

import csv
import sys
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import config


class LikedSongsFilter:
    def __init__(self, popularity_threshold=80):
        """
        Initialize the liked songs filter.
        
        Args:
            popularity_threshold: Minimum popularity score (0-100).
                                 ~80+ = very popular (>200M streams equivalent)
        """
        if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
            raise ValueError(
                "Spotify credentials not found. Set SPOTIFY_CLIENT_ID "
                "and SPOTIFY_CLIENT_SECRET in .env file"
            )
        
        self.sp = Spotify(
            auth_manager=SpotifyOAuth(
                scope="user-library-read",
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
                redirect_uri="http://127.0.0.1:8888",
                cache_path=".spotify_cache"
            )
        )
        self.popularity_threshold = popularity_threshold
    
    def get_filtered_liked_songs(self):
        """
        Fetch all liked songs and filter by popularity threshold.
        
        Returns:
            List of dicts with keys: name, artist, album, popularity, url, year
        """
        liked = []
        results = self.sp.current_user_saved_tracks(limit=50)
        
        print(f"Fetching liked songs (popularity >= {self.popularity_threshold})...")
        
        while results:
            for item in results["items"]:
                track = item["track"]
                if track and track["popularity"] >= self.popularity_threshold:
                    artists = ", ".join([a["name"] for a in track["artists"]])
                    release_date = track["album"]["release_date"]
                    year = release_date.split("-")[0] if release_date else "Unknown"
                    
                    liked.append({
                        "name": track["name"],
                        "artist": artists,
                        "album": track["album"]["name"],
                        "popularity": track["popularity"],
                        "url": track["external_urls"]["spotify"],
                        "year": year
                    })
            
            # Pagination
            results = self.sp.next(results) if results["next"] else None
        
        return liked
    
    def save_to_csv(self, songs, filename="liked_songs_filtered.csv"):
        """
        Save filtered songs to a CSV file.
        
        Args:
            songs: List of song dictionaries
            filename: Output CSV filename
        """
        if not songs:
            print("No songs to save!")
            return
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "artist", "album", "year", "popularity", "url"])
            writer.writeheader()
            writer.writerows(songs)
        
        print(f"\n✓ Saved {len(songs)} songs to {filename}")


def main():
    """CLI interface for filtering liked songs."""
    try:
        # Parse command line arguments
        popularity_threshold = 80  # Default
        output_file = None
        
        args = sys.argv[1:]
        i = 0
        while i < len(args):
            if args[i] == "--popularity" and i + 1 < len(args):
                popularity_threshold = int(args[i + 1])
                i += 2
            elif args[i] == "--output" and i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
            else:
                i += 1
        
        # Fetch and filter songs
        filter_client = LikedSongsFilter(popularity_threshold=popularity_threshold)
        songs = filter_client.get_filtered_liked_songs()
        
        if not songs:
            print(f"\nNo liked songs found with popularity >= {popularity_threshold}")
            return []
        
        print(f"\n✓ Found {len(songs)} songs with popularity >= {popularity_threshold}")
        
        # Save to CSV if output file specified
        if output_file:
            filter_client.save_to_csv(songs, output_file)
        else:
            # Print to console
            print("\n" + "="*80)
            print(f"{'ARTIST':<30} {'SONG':<35} {'POP':<5} {'YEAR':<5}")
            print("="*80)
            for track in songs:
                artist = track["artist"][:28]
                name = track["name"][:33]
                print(f'{artist:<30} {name:<35} {track["popularity"]:<5} {track["year"]:<5}')
            print("="*80)
        
        return songs
    
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

