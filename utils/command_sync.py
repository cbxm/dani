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

# Example usage in main.py:
# 
# from utils.command_sync import sync_commands
# 
# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user}')
#     await sync_commands(bot, GUILD_ID)  # For guild-specific commands
#     # or
#     # await sync_commands(bot)  # For global commands