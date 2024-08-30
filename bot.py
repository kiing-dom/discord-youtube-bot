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


bot = commands.Bot(command_prefix='!', intents=intents)

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_channel_stats(channel_identifier):
    try:
        # Check if the identifier is a new-style username (starts with @)
        if channel_identifier.startswith('@'):
            # Search for the channel
            search_response = youtube.search().list(
                part="snippet",
                q=channel_identifier,
                type="channel",
                maxResults=1
            ).execute()

            if 'items' in search_response and len(search_response['items']) > 0:
                channel_id = search_response['items'][0]['id']['channelId']
            else:
                return None
        elif channel_identifier.startswith('UC'):
            channel_id = channel_identifier
        else:
            # Assume it's an old-style username
            channel_id = None

        # Get channel details
        if channel_id:
            request = youtube.channels().list(
                part="statistics,snippet",
                id=channel_id
            )
        else:
            request = youtube.channels().list(
                part="statistics,snippet",
                forUsername=channel_identifier
            )
        
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            title = channel['snippet']['title']
            subs = channel['statistics']['subscriberCount']
            views = channel['statistics']['viewCount']
            videos = channel['statistics']['videoCount']
            thumbnail = channel['snippet']['thumbnails']['high']['url']
            return title, subs, views, videos, thumbnail
        else:
            return None
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def search_youtube_videos(query):
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=5
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail = item['snippet']['thumbnails']['high']['url']
            videos.append((title, video_url, thumbnail))
        return videos
    
    except HttpError:
        return None
    except Exception:
        return None

def get_video_details(video_id):
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            title = video['snippet']['title']
            views = video['statistics']['viewCount']
            likes = video['statistics'].get('likeCount', 'N/A')
            comments = video['statistics'].get('commentCount', 'N/A')
            thumbnail = video['snippet']['thumbnails']['high']['url']
            return title, views, likes, comments, thumbnail
        else:
            return None
    
    except HttpError:
        return None
    except Exception:
        return None

def get_latest_video(channel_identifier):
    try:
        # Check if the identifier is a new-style username (starts with @)
        if channel_identifier.startswith('@'):
            # Search for the channel
            search_response = youtube.search().list(
                part="snippet",
                q=channel_identifier,
                type="channel",
                maxResults=1
            ).execute()

            if 'items' in search_response and len(search_response['items']) > 0:
                channel_id = search_response['items'][0]['id']['channelId']
            else:
                return None
        elif channel_identifier.startswith('UC'):
            channel_id = channel_identifier
        else:
            # Assume it's an old-style username
            channel_id = None

        if not channel_id:
            return None

        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            maxResults=1
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            title = video['snippet']['title']
            video_id = video['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            thumbnail = video['snippet']['thumbnails']['high']['url']
            return title, video_url, thumbnail
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
async def ytstats(ctx, channel_identifier):
    stats = get_channel_stats(channel_identifier)
    
    if stats:
        title, subs, views, videos, thumbnail = stats
        embed = discord.Embed(
            title=f'{title} YouTube Channel Stats',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Subscribers", value=subs, inline=True)
        embed.add_field(name="Total Views", value=views, inline=True)
        embed.add_field(name="Video Count", value=videos, inline=True)
    else:
        embed = discord.Embed(
            title="Error",
            description="Could not retrieve data for the provided channel ID or username. Please check if the ID or username is correct.",
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

@bot.command()
async def ytsearch(ctx, *, query):
    videos = search_youtube_videos(query)

    if videos:
        embed = discord.Embed(
            title="Top 5 YouTube Videos",
            description=f"Search results for: {query}",
            color=discord.Color.red()
        )
        for title, url, thumbnail in videos:
            embed.add_field(name=title, value=url, inline=False)
            embed.set_image(url=thumbnail)
    else:
        embed = discord.Embed(
            title="Error",
            description="Could not find any videos matching your query.",
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

@bot.command()
async def ytvideo(ctx, video_id):
    video = get_video_details(video_id)

    if video:
        title, views, likes, comments, thumbnail = video
        embed = discord.Embed(
            title=title,
            url=f"https://www.youtube.com/watch?v={video_id}",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Views", value=views, inline=True)
        embed.add_field(name="Likes", value=likes, inline=True)
        embed.add_field(name="Comments", value=comments, inline=True)
    else:
        embed = discord.Embed(
            title="Error",
            description="Could not retrieve data for the provided video ID. Please check if the ID is correct.",
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

@bot.command()
async def ytlatest(ctx, channel_id):
    video = get_latest_video(channel_id)

    if video:
        title, video_url, thumbnail = video
        embed = discord.Embed(
            title="Latest Video",
            description=f"[{title}]({video_url})",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=thumbnail)
    else:
        embed = discord.Embed(
            title="Error",
            description="Could not retrieve the latest video for the provided channel ID.",
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

# Start the Discord bot
bot.run(DISCORD_TOKEN)
