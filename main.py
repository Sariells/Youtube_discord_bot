import discord
from discord.ext import commands
import yt_dlp
import subprocess
import asyncio
import time
import os
TOKEN = 'TOKEN' 


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',  
        'extractaudio': True,
        'audioquality': 1,
        'prefer_ffmpeg': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info)  
        return audio_file

@bot.command()
async def play(ctx, url: str):
    await ctx.send(f"Скачиваю и воспроизводим аудио с {url}")

    # Скачиваем аудио с YouTube
    audio_file = download_audio(url)

    # Проверим, существует ли файл
    if not os.path.exists(audio_file):
        await ctx.send("Ошибка при скачивании аудио!")
        return

    ffmpeg_command = [
        'ffmpeg',
        '-i', audio_file,
        '-f', 'wav',
        '-ac', '1',  
        '-ar', '44100',  
        'Line 1 (Virtual Audio Cable)' 
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    await asyncio.sleep(1)  

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    voice_client.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: print('done', e))

    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)