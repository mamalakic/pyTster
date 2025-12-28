# Spotify Playlist Board Game - Card Generator

Python scraper program that creates printable QR cards for the board game "Hitster"

## How It Works

### 1. Card Generator
1. **Input**: Players provide their Spotify playlist URLs
2. **Fetch**: Program retrieves songs from each playlist
3. **Generate**: Creates a printable PDF with:
   - **Front side**: QR code linking to the Spotify song
   - **Back side**: Song details (year, title, artists) at matching coordinates

### 2. Liked Songs Filter
- Fetch all your Spotify liked songs
- Filter by popularity (0-100 scale, ~80+ = >200M streams)
- Export to CSV or pass as object
- Useful for finding your most popular liked tracks

## Requirements

- Python 3.7+
- Spotify Developer Account (free)

## Setup

### 1. Dependencies

```bash
pip install -r requirements.txt
```

### 2. Spotify API Credentials

1. [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with Spotify account
3. Click "Create an App"
4. Give it a name
5. Copy **Client ID** and **Client Secret**

### 3. Configure Environment

Create an `.env` file in the project directory with:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

## Usage

### Option 1: Interactive Menu

```bash
python main.py
```

Choose your mode:
1. **Generate cards from playlists**
2. **Filter liked songs by popularity**

### Option 2: Standalone Liked Songs Filter

```bash
# Print to console (default popularity >= 80)
python filter_liked_songs.py

# Save to CSV
python filter_liked_songs.py --output liked.csv

# Custom popularity threshold
python filter_liked_songs.py --popularity 90 --output my_popular_songs.csv
```

### Playlist Mode Instructions:
1. Enter each player's Spotify playlist URL
2. Press Enter when done adding playlists
3. Choose how many songs per playlist (default: 10)


## Output

Creates `game_cards.pdf` with:
- **Odd pages**: QR codes (front of cards)
- **Even pages**: Song information (back of cards)

## Printing Instructions

1. Print **odd pages only** (pages with QR codes)
2. Take the printed pages and flip the entire stack
3. Reinsert the paper into your printer
4. Print **even pages only** (pages with song info)
5. Cut along the gray borders to separate cards

## Configuration

Edit `config.py` to customize:

```python
SONGS_PER_PLAYLIST = 10      # Default songs per playlist
MIN_TRACK_POPULARITY = 80     # Minimum popularity for playlist songs
QR_SIZE = 200                # QR code size in pixels
CARDS_PER_PAGE = 6           # Cards per page (2×3 grid)
MARGIN = 18                  # Page margin in points (0.25 inch)
```

## Troubleshooting

**"Spotify credentials not found"**
- Make sure you created a `.env` file with your credentials

**"No songs were fetched"**
- Check that playlist URLs are correct
- Make sure the playlists are public or you have access

**Liked Songs Authentication**
- First time running liked songs filter requires browser login
- A `.spotify_cache` file will be created to store your auth token
- Add `http://127.0.0.1:8888` to your Spotify app's redirect URIs if needed

## Notes

- Playlist URLs can be in format: `https://open.spotify.com/playlist/XXXXX`
- Or just the playlist ID: `XXXXX`
- The program handles both main artists and featured artists
- Spotify doesn't expose exact play counts/views - popularity is their internal metric
- The liked songs filter can be imported and used programmatically:
  ```python
  from liked_songs_filter import LikedSongsFilter
  
  filter_client = LikedSongsFilter(popularity_threshold=85)
  songs = filter_client.get_filtered_liked_songs()
  # Returns list of dicts with: name, artist, album, popularity, url, year
  ```
