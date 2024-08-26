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