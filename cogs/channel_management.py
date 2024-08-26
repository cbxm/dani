# cogs/channel_management.py

import discord
from discord import app_commands
from discord.ext import commands
from utils.emoji_helpers import extract_emoji
import asyncio

class ChannelManagement(commands.Cog):
    """
    A cog that provides channel management commands for a Discord bot.
    """

    def __init__(self, bot):
        self.bot = bot

    # Create a command group for channel management commands
    chan_group = app_commands.Group(name="chan", description="Channel management commands")

    async def process_channels(self, interaction: discord.Interaction, process_func):
        """
        Process all text channels in the guild using the provided function.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
            process_func (callable): A function that processes a single channel.

        This method handles batching, progress updates, and error handling for channel processing.
        """
        await interaction.response.defer(ephemeral=True)
        
        updated_channels = 0
        total_channels = len(interaction.guild.channels)
        
        async def update_channel(channel):
            """
            Update a single channel and handle any errors.

            Args:
                channel (discord.abc.GuildChannel): The channel to update.
            """
            nonlocal updated_channels
            try:
                result = await process_func(channel)
                if result:
                    updated_channels += 1
            except discord.Forbidden:
                await interaction.followup.send(f"Failed to update {channel.name}. Missing permissions.", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.followup.send(f"Failed to update {channel.name}. Error: {str(e)}", ephemeral=True)

        # Create update tasks for all text channels
        update_tasks = [update_channel(channel) for channel in interaction.guild.channels if isinstance(channel, discord.TextChannel)]
        
        # Process channels in batches of 10
        for i in range(0, len(update_tasks), 10):
            batch = update_tasks[i:i+10]
            await asyncio.gather(*batch)
            
            # Send progress update every 50 channels or at the end
            if (i + 10) % 50 == 0 or i + 10 >= len(update_tasks):
                progress = min((i + 10) / total_channels * 100, 100)
                await interaction.followup.send(f"Progress: {progress:.2f}% ({updated_channels}/{total_channels} channels processed)", ephemeral=True)
        
        await interaction.followup.send(f"Finished! Updated {updated_channels} channel(s).", ephemeral=True)

    @chan_group.command(name="paint", description="Update channel titles to match category emoji")
    async def chan_paint(self, interaction: discord.Interaction):
        """
        Add emoji prefixes to channel names based on their category's emoji.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
        """
        async def paint_channel(channel):
            """
            Add emoji prefix to a single channel's name.

            Args:
                channel (discord.TextChannel): The channel to update.

            Returns:
                bool: True if the channel was updated, False otherwise.
            """
            category = channel.category
            if category:
                category_emoji = extract_emoji(category.name)
                if category_emoji:
                    new_name = f"{category_emoji}┋{channel.name.split('┋')[-1]}"
                    if channel.name != new_name:
                        await channel.edit(name=new_name)
                        return True
            return False

        await self.process_channels(interaction, paint_channel)

    @chan_group.command(name="strip", description="Remove emoji prefixes from all channel titles")
    async def chan_strip(self, interaction: discord.Interaction):
        """
        Remove emoji prefixes from all channel names.

        Args:
            interaction (discord.Interaction): The interaction that triggered the command.
        """
        async def strip_channel(channel):
            """
            Remove emoji prefix from a single channel's name.

            Args:
                channel (discord.TextChannel): The channel to update.

            Returns:
                bool: True if the channel was updated, False otherwise.
            """
            if '┋' in channel.name:
                new_name = channel.name.split('┋')[-1]
                if channel.name != new_name:
                    await channel.edit(name=new_name)
                    return True
            return False

        await self.process_channels(interaction, strip_channel)

async def setup(bot):
    """
    Set up the ChannelManagement cog.

    Args:
        bot (commands.Bot): The bot instance to add this cog to.
    """
    await bot.add_cog(ChannelManagement(bot))

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
    """Load all cog extensions."""
    await bot.load_extension('cogs.channel_management')

async def main():
    """Main function to start the bot."""
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'Logged in as {bot.user}')
    await sync_commands(bot, GUILD_ID)  # Sync commands to the specific guild

# Run the bot
asyncio.run(main())

# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Discord bot token and guild ID from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

# utils/emoji_helpers.py

import re

def extract_emoji(text):
    """
    Extract the first emoji from the given text.

    Args:
        text (str): The text to extract emoji from.

    Returns:
        str or None: The first emoji found in the text, or None if no emoji is found.
    """
    emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]")
    match = emoji_pattern.search(text)
    return match.group(0) if match else None

# utils/command_sync.py

import discord
from discord import app_commands
from typing import Optional, List

async def sync_commands(bot: discord.Client, guild_id: Optional[int] = None):
    """
    Sync application commands with Discord.
    
    Args:
    bot (discord.Client): The bot instance.
    guild_id (Optional[int]): The ID of the guild to sync commands to. 
                              If None, syncs globally.
    
    Returns:
    List[app_commands.Command]: The list of synced commands.
    """
    if guild_id:
        guild = discord.Object(id=guild_id)
        bot.tree.copy_global_to(guild=guild)
        synced_commands = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced_commands)} commands to guild with ID {guild_id}")
    else:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands globally")
    
    return synced_commands