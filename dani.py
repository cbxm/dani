# main.py
import discord
from discord.ext import commands
import asyncio
from config import TOKEN, GUILD_ID
from utils.command_sync import sync_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    await bot.load_extension('cogs.channel_management')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await sync_commands(bot, GUILD_ID)  # Sync commands to the specific guild

asyncio.run(main())
