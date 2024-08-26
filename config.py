# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Discord bot token from environment variables
# This token should be kept secret and never shared publicly
TOKEN = os.getenv('DISCORD_TOKEN')

# Get guild ID from environment variables and convert it to an integer
# This is used for guild-specific command syncing
GUILD_ID = int(os.getenv('GUILD_ID'))