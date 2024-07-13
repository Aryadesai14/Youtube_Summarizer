# video_summarizer/views.py

import openai
from django.shortcuts import render
from django.http import JsonResponse
from decouple import config
from googleapiclient.discovery import build
import json

# Load the API keys from environment variables
openai.api_key = config('OPENAI_API_KEY')
youtube_api_key = config('YOUTUBE_API_KEY')

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    video_info = response['items'][0]['snippet']['description']
    return video_info

def summarize_video(video_url):
    try:
        # Extract the video ID from the URL
        video_id = video_url.split('v=')[1]
        video_info = get_video_info(video_id)

        # Call the OpenAI API to summarize the video description
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Summarize the following YouTube video description in its original language and in English:\n\n{video_info}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error communicating with OpenAI API: {e}"

def index(request):
    return render(request, 'video_summarizer/index.html')

# Define the view function for summarizing videos
import requests
from django.http import JsonResponse
from urllib3.exceptions import InsecureRequestWarning

def summarize(request):
    video_url = request.POST.get('video_url')

    import requests

# Replace with your actual OpenAI API key
api_key = 'your_actual_openai_api_key'
url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

data = {
    'prompt': 'Once upon a time,',
    'max_tokens': 50,
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    print(response.json())
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # Print HTTP error details
    print(f"Response content: {response.content}")
except Exception as err:
    print(f"Other error occurred: {err}")  # Print any other error details

       

