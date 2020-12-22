# Specifications: accept a channelid as a input
# Move everyone in that channel to a target channel

import discord
import argparse

from dotenv import load_dotenv
import os

load_dotenv()

from discord import FFmpegPCMAudio, VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context

from typing import cast
import asyncio

CMD_CHANNEL_ID = 790772134016188476
AUDIO_CHANNEL_ID = 790829385606234112
TARGET_CHANNEL_ID = 790829461816999946

PRESIDENT_ROLE = "Admin"

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(guilds=True, voice_states=True, messages=True)
bot = commands.Bot(command_prefix="~", intents=intents)
# bot = commands.Bot(command_prefix="~")


@bot.command()
async def playmugs(ctx: Context):
    # Filter based on channel source and author role
    author_roles = [role.name for role in ctx.message.author.roles]
    if (ctx.message.channel.id != CMD_CHANNEL_ID    
            or PRESIDENT_ROLE not in author_roles):
        return

    # Play mug sounds
    vc = cast(VoiceClient, ctx.voice_client)
    vc.play(FFmpegPCMAudio("assets/zelda.mp3"))
    while vc.is_playing():
        await asyncio.sleep(0.01)

    # Add a sleep here if desired

    voice_chann = cast(VoiceChannel, ctx.voice_client.channel)
    target_channel = await bot.fetch_channel(TARGET_CHANNEL_ID)
    print(voice_chann.members)
    for user in voice_chann.members:
        if user.id == bot.user.id:
            continue
        await user.move_to(target_channel)
    # await bot.logout()

@bot.event
async def on_ready():
    # Join the target channel on bot start
    await bot.get_channel(AUDIO_CHANNEL_ID).connect()
    print("Ready!")

bot.run(DISCORD_TOKEN)