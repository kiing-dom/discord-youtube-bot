import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load the .env file
load_dotenv()

# Get the tokens
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Check if tokens are available
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Use commands.Bot instead of discord.Client for easier command handling
bot = commands.Bot(command_prefix='!', intents=intents)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_channel_stats(channel_id):
    try:
        request = youtube.channels().list(
            part="statistics,snippet",
            id=channel_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            title = channel['snippet']['title']
            subs = channel['statistics']['subscriberCount']
            views = channel['statistics']['viewCount']
            videos = channel['statistics']['videoCount']
            return title, subs, views, videos
        else:
            return None
        
    except HttpError:
        return None
    except Exception:
        return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command()
async def ytstats(ctx, channel_id):
    stats = get_channel_stats(channel_id)
    
    if stats:
        title, subs, views, videos = stats
        response = (f'**{title}** YouTube Channel Stats:\n'
                    f'Subscribers: {subs}\n'
                    f'Total Views: {views}\n'
                    f'Video Count: {videos}')
    else:
        response = 'Could not retrieve data for the provided channel ID. Please check if the ID is correct.'

    try:
        await ctx.send(response)
    except discord.errors.HTTPException:
        await ctx.send("An error occurred while sending the message. Please try again.")
    except Exception:
        await ctx.send("An unexpected error occurred. Please try again later.")

# New command: ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# New command: echo
@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

# New command: serverinfo
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    num_members = server.member_count
    server_name = server.name
    server_owner = server.owner
    response = (f'**Server Name:** {server_name}\n'
                f'**Owner:** {server_owner}\n'
                f'**Member Count:** {num_members}')
    await ctx.send(response)

# Start the Discord bot
bot.run(DISCORD_TOKEN)
