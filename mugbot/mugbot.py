import asyncio
import os
from typing import cast

import discord
from discord import FFmpegPCMAudio, VoiceChannel, VoiceClient
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

# Channel id to listen for commands from
CMD_CHANNEL_ID = 790772134016188476
# Voice channel id to E X I S T in
AUDIO_CHANNEL_ID = 790829385606234112
# Voice channel id to move members to after playing
TARGET_CHANNEL_ID = 790829461816999946

# Only the president can use the mugs
PRESIDENT_ROLE = "Admin"

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# guilds - required for bot to function
# voice_states - list members in voice channel
# messages - see text command
intents = discord.Intents(guilds=True, voice_states=True, messages=True)
bot = commands.Bot(command_prefix="~", intents=intents)


@bot.command()
async def playmugs(ctx: Context):
    # Filter based on channel source and author role
    author_roles = [role.name for role in ctx.message.author.roles]
    if (ctx.message.channel.id != CMD_CHANNEL_ID
            or PRESIDENT_ROLE not in author_roles):
        return

    # Play mug sounds
    vc = cast(VoiceClient, ctx.voice_client)
    print("Playing music")
    vc.play(FFmpegPCMAudio("assets/mugs.mp3"))
    while vc.is_playing():
        await asyncio.sleep(0.01)
    print("Music done")

    # Add a sleep here if desired

    voice_chann = cast(VoiceChannel, ctx.voice_client.channel)
    target_channel = await bot.fetch_channel(TARGET_CHANNEL_ID)
    # NOTE: this only moves members that joined after the bot
    print(voice_chann.members)
    for user in voice_chann.members:
        if user.id == bot.user.id:
            continue
        await user.move_to(target_channel)


@bot.event
async def on_ready():
    # Join the target channel on bot start
    await bot.get_channel(AUDIO_CHANNEL_ID).connect()
    print("Ready!")


bot.run(DISCORD_TOKEN)
