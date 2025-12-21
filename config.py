"""Configuration settings for the Spotify playlist game."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Game settings
SONGS_PER_PLAYLIST = 10  # Default number of songs to fetch per playlist
MIN_TRACK_POPULARITY = 0  # Minimum popularity score (0-100). Higher = more popular/views
QR_SIZE = 200  # QR code size in pixels
CARDS_PER_PAGE = 6  # Number of cards per page (2x3 grid)

# PDF settings
PAGE_WIDTH = 612  # Letter size in points (8.5 inches)
PAGE_HEIGHT = 792  # Letter size in points (11 inches)
MARGIN = 18  # 0.25 inch margin (tighter to save space)

