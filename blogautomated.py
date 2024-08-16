import os
import time
import requests
import sqlite3
import sys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import json

YOUTUBE_API_KEY = 'AIzaSyBWogKI1u80ZF6j6eUIjJ2GZSX1F8fjSgk'# Replace with your youtube api key
CHANNEL_ID = os.getenv('CHANNEL_ID')# Replace with your youtube channel id to convert into blog
GEMINI_API_KEY = os.getenv('GEMINI')  # Replace with your Gemini API key
MEDIUM_INTEGRATION_TOKEN = os.getenv('MEDIUM')# Replace with your medium integration token
print(YOUTUBE_API_KEY)
# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Configure Google Generative AI
genai.configure(api_key=GEMINI_API_KEY)

# Initialize database
DB_FILE = 'videos.db'
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS published_videos (video_id TEXT PRIMARY KEY)''')
conn.commit()

def get_medium_user_id(integration_token):
    url = "https://api.medium.com/v1/me"
    headers = {
        "Authorization": f"Bearer {integration_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data['data']['id']
        return user_id
    else:
        print(f"Failed to retrieve user data: {response.status_code}")
        return None
mediumuserId=get_medium_user_id(MEDIUM_INTEGRATION_TOKEN)
def get_latest_video(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def download_subtitle(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript_list])
    except Exception as e:
        print(f"Failed to download subtitle for video {video_id}: {e}")
        sys.exit()
        return None

def analyze_transcript(transcript, video_id):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Convert this subtitle into a script: {transcript}")
    script_text = response._result

    response2 = model.generate_content(
        f"You are a professional blog writer. "
        f"Convert the script into a SEO optimized professional HTML blog with relevant keyword . Write the blog not in the first person. Convey in your own way. "
        f"Divide it into paragraphs. Here is the script: {script_text}. "
    )
    return response2.text

def publish_to_medium(title, content):
    url = "https://api.medium.com/v1/users/"+mediumuserId+"/posts"
    tags=["","","","",""] #insert your tags here
    headers = {
        'Authorization': f'Bearer {MEDIUM_INTEGRATION_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        'title': title,
        'contentFormat': 'html',
        'content': content,
        'tags':tags,
        'publishStatus': 'public'
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Published to Medium successfully. Status code: {response.status_code}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")

def process_new_video():
    video = get_latest_video(CHANNEL_ID)
    if video:
        video_id = video['id']['videoId']

        # Check if video was already processed
        c.execute('SELECT video_id FROM published_videos WHERE video_id = ?', (video_id,))
        if c.fetchone():
            print(f"Video {video_id} already processed.")
            return
        print("processing video")
        title = video['snippet']['title']
        
        subtitle = download_subtitle(video_id)
        analysis = analyze_transcript(subtitle, video_id)
        publish_to_medium(title,analysis)
        c.execute('INSERT INTO published_videos (video_id) VALUES (?)', (video_id,))
        conn.commit()

process_new_video()
