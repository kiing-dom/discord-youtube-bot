import os
import discord
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

DISCORD_TOKEN = os.get('DISCORD_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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
        
    except Exception as e:
        print(f"Error fetching the YouTube channel stats: {e}")
        return None