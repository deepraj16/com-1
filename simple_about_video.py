import pandas as pd 
import numpy as np  

from googleapiclient.discovery import build
import datetime
from urllib.parse import urlparse,parse_qs 

def extract_video_id(url):
    parsed_url = urlparse(url)
    
    if 'youtube' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    
    return None

def simple_info(url):
    api_key = "AIzaSyAIoH57hvboq-foyUPKP9Ihz4UHYj6FC-0"
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id=extract_video_id(url)
    video_response = youtube.videos().list(
        part='statistics,snippet,contentDetails,status',
        id=video_id
    ).execute()
    video = video_response['items'][0]
    info={

        "video_id": video['id'],
        "Title:": video['snippet']['title'],
        "Published At:": video['snippet']['publishedAt'],
        "Channel:": video['snippet']['channelTitle'],
        "Views:": video['statistics']['viewCount'],
        "Likes:": video['statistics'].get('likeCount', 'N/A'),
        "Comments:": video['statistics'].get('commentCount', 'N/A'),
        "Duration:": video['contentDetails']['duration'],
        "Privacy Status:": video['status']['privacyStatus'],
    }
    return info



# url="https://youtu.be/m9s1NQG3TNY?feature=shared" 
# print(simple_info(url))

# for i in simple_info(url).items():
#     print(i[0],i[1])