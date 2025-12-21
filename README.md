# Spotify Playlist Board Game - Card Generator

Python scraper program that creates printable QR cards for the board game "Hitster"

## How It Works

1. **Input**: Players provide their Spotify playlist URLs
2. **Fetch**: Program retrieves songs from each playlist
3. **Generate**: Creates a printable PDF with:
   - **Front side**: QR code linking to the Spotify song
   - **Back side**: Song details (year, title, artists) at matching coordinates

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

## 4. Run the program:

```bash
python main.py
```

## 5. Follow the prompts:
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

## Notes

- Playlist URLs can be in format: `https://open.spotify.com/playlist/XXXXX`
- Or just the playlist ID: `XXXXX`
- The program handles both main artists and featured artists
