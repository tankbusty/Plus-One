import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COPY_EMOJI_IDS = {
    1487653182644686941,
    1500959260392161382,
    935551452850577408,
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if payload.emoji.id not in COPY_EMOJI_IDS:
        return

    channel = await bot.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)

    user = payload.member or await bot.fetch_user(payload.user_id)

    if not message.content and not message.attachments:
        return

    files = [await a.to_file() for a in message.attachments] if message.attachments else []

    await channel.send(
        content=f"💬 **{user.name}**:\n{message.content}",
        files=files,
        allowed_mentions=discord.AllowedMentions.none()
    )

print("BOT STARTING...")
bot.run(os.environ["TOKEN"])
