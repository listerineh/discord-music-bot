import os
import discord
import youtube_dl

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.voice_states = True

bot = commands.Bot(command_prefix='t.', intents=intents)

@bot.event
async def on_ready():
    print('Bot is online!')

@bot.command()
async def play(ctx, url):
    print('play')
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send('You need to be in a voice channel to play music!')
        return

    try:
        voice_client = await voice_channel.connect()
    except discord.errors.ClientException:
        voice_client = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url2))

    await ctx.send(f'Now playing: {url}')


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


if __name__ == '__main__':
    try:
        bot_token = os.getenv('BOT_TOKEN')
        bot.run(bot_token)
    except Exception as e:
        print(f'Unexpected error: {e}')
