# main.py

import discord
from discord.ext import commands
import asyncio
from config import TOKEN, GUILD_ID
from utils.command_sync import sync_commands

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    """
    Load all cog extensions.
    
    This function is responsible for loading all the cogs (extension modules)
    that contain the bot's commands and listeners.
    """
    await bot.load_extension('cogs.channel_management')
    # Add any additional cogs here as needed

async def main():
    """
    Main function to start the bot.
    
    This function sets up the bot by loading extensions and starting the bot
    with the provided token.
    """
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    
    This function is called when the bot has successfully connected to
    Discord and is ready to receive commands. It prints a login confirmation
    and syncs the bot's slash commands with Discord.
    """
    print(f'Logged in as {bot.user}')
    await sync_commands(bot, GUILD_ID)  # Sync commands to the specific guild

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())