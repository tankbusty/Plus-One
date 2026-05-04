import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COPY_EMOJI_IDS = {
    1487653182644686941,
    1500551597288325381,
    1500959260392161382	  
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    # only trigger for allowed emojis
    if payload.emoji.id not in COPY_EMOJI_IDS:
        return

    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return

    message = await channel.fetch_message(payload.message_id)

    user = await bot.fetch_user(payload.user_id)

    if not message.content and not message.attachments:
        return

    files = []
    if message.attachments:
        files = [await a.to_file() for a in message.attachments]

    # ⭐ Option 1 behavior: reactor "appears" as the speaker
    await channel.send(
        content=f"💬 **{user.display_name}**:\n{message.content}",
        files=files,
        allowed_mentions=discord.AllowedMentions.none()
    )
import os
bot.run(os.environ["TOKEN"])