import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COPY_EMOJI = "1487653182644686941"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if str(payload.emoji) != COPY_EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)

    if not channel:
        return

    message = await channel.fetch_message(payload.message_id)

    user = guild.get_member(payload.user_id)
    if not user:
        user = await bot.fetch_user(payload.user_id)

    if not message.content and not message.attachments:
        return

    files = []
    if message.attachments:
        files = [await a.to_file() for a in message.attachments]

    await channel.send(
        f"📋 {user.mention} copied a message from {message.author.mention}:\n{message.content}",
        files=files
    )

@bot.event
async def on_raw_reaction_add(payload):
    print("REACTION DETECTED")
import os
bot.run(os.environ["TOKEN"])