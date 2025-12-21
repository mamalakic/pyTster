import sys
from spotify_client import SpotifyClient
from pdf_generator import PDFGenerator
import config


def get_playlist_urls():
    print("\n=== Spotify Playlist Board Game - Card Generator ===\n")
    print("Generate printable cards with QR codes and song info.\n")
    
    playlists = []
    while True:
        player_num = len(playlists) + 1
        print(f"\nPlayer {player_num}:")
        url = input("  Enter Spotify playlist URL (or press Enter to finish): ").strip()
        
        if not url:
            if not playlists:
                print("  Error: Need at least one playlist!")
                continue
            break
        
        playlists.append(url)
        print(f"  ✓ Added playlist for Player {player_num}")
    
    return playlists


def get_songs_per_playlist():
    default = config.SONGS_PER_PLAYLIST
    response = input(f"\nHow many songs per playlist? (default: {default}): ").strip()
    
    if not response:
        return default
    
    try:
        num = int(response)
        return num if num > 0 else default
    except ValueError:
        return default


def main():
    try:
        if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
            print("\nERROR: Spotify API credentials not found!")
            print("\nSteps:")
            print("1. Go to https://developer.spotify.com/dashboard")
            print("2. Create an app")
            print("3. Create .env file with:")
            print("   SPOTIFY_CLIENT_ID=your_client_id")
            print("   SPOTIFY_CLIENT_SECRET=your_client_secret")
            sys.exit(1)
        
        playlist_urls = get_playlist_urls()
        songs_per_playlist = get_songs_per_playlist()
        
        print(f"\n{'='*60}")
        print(f"Players: {len(playlist_urls)} | Songs per playlist: {songs_per_playlist}")
        print(f"Total songs: {len(playlist_urls) * songs_per_playlist}")
        print(f"{'='*60}\n")
        
        print("Connecting to Spotify...")
        spotify = SpotifyClient()
        songs = spotify.get_multiple_playlists(playlist_urls, songs_per_playlist)
        
        if not songs:
            print("\nERROR: No songs fetched. Check playlist URLs.")
            sys.exit(1)
        
        print(f"\n✓ Fetched {len(songs)} songs")
        
        output_file = "game_cards.pdf"
        print(f"\nGenerating PDF: {output_file}")
        
        pdf_gen = PDFGenerator()
        pdf_gen.generate_pdf(songs, output_file)
        
        print("\n" + "="*60)
        print("✓ SUCCESS! Your game cards are ready!")
        print("="*60)
        print(f"\nFile: {output_file} | Cards: {len(songs)}")

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
