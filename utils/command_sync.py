# command_sync.py

import discord
from discord import app_commands
from typing import Optional, List

async def sync_commands(bot: discord.Client, guild_id: Optional[int] = None):
    """
    Sync application commands with Discord.
    
    This function syncs the bot's slash commands with Discord, either globally
    or for a specific guild. Syncing is necessary for slash commands to appear
    and function correctly in Discord.

    Args:
    bot (discord.Client): The bot instance.
    guild_id (Optional[int]): The ID of the guild to sync commands to. 
                              If None, syncs globally.
    
    Returns:
    List[app_commands.Command]: The list of synced commands.
    """
    if guild_id:
        # Sync commands to a specific guild
        guild = discord.Object(id=guild_id)
        bot.tree.copy_global_to(guild=guild)
        synced_commands = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced_commands)} commands to guild with ID {guild_id}")
    else:
        # Sync commands globally
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands globally")
    
    return synced_commands