import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Discord Bot Token
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# YouTube Data API Key (Optional)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Spotify API Credentials (Optional)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# SoundCloud API Credentials (Optional)
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")
SOUNDCLOUD_CLIENT_SECRET = os.getenv("SOUNDCLOUD_CLIENT_SECRET")

# Other configuration settings (as needed)
# ...