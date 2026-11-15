import discord
from discord.ext import commands
from gtts import gTTS
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"تم الانضمام إلى روم: {channel.name}")
    else:
        await ctx.send("يجب أن تكون في روم صوتية أولاً!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الخروج من الروم الصوتية.")
    else:
        await ctx.send("البوت ليس في أي روم صوتية حالياً.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if message.guild:
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_connected() and not voice_client.is_playing():
            try:
                tts = gTTS(text=message.content, lang='ar')
                tts.save("speech.mp3")
                voice_client.play(discord.FFmpegPCMAudio("speech.mp3"), after=lambda e: os.remove("speech.mp3") if os.path.exists("speech.mp3") else None)
            except Exception as e:
                print(f"TTS Error: {e}")

    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
