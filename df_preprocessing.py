import pandas as pd 
import numpy as np 
from googleapiclient.discovery import build 
from urllib.parse import urlparse,parse_qs 
from collections import Counter

import datetime

from textblob import TextBlob

def extract_video_id(url):
    parsed_url = urlparse(url)
    
    if 'youtube' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    
    # Case 2: https://youtu.be/oDI1OKz5TGU
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    
    return None

def get_comments(video_id):
    comments = []
    api_key = "AIzaSyAIoH57hvboq-foyUPKP9Ihz4UHYj6FC-0"
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_text = snippet["textDisplay"]
            comment_time = snippet["publishedAt"]

            comment_time = datetime.datetime.strptime(comment_time, "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = comment_time.strftime("%Y-%m-%d %H:%M:%S")

            comments.append((comment_text, formatted_time))
        if(len(comments)==6000): 
            return comments
        request = youtube.commentThreads().list_next(request, response)

    return comments


def classify_sentiment(comment):
    polarity = TextBlob(str(comment)).sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.05:
        return 'negative'
    else:
        return 'Normal'
    

def create_df(comments): 
    date=[]
    message=[]
    for i in comments: 
        date.append(i[1])
        message.append(i[0])

    df=pd.DataFrame({
        'message': message , 
        'date'  : date
    })
    df['date_time'] = pd.to_datetime(df['date'])
    df['Sentiment'] = df['message'].apply(classify_sentiment)
    df['year']=df['date_time'].dt.year
    df['month']=df['date_time'].dt.month_name()
    df['day']=df['date_time'].dt.day_name()
    df=df.drop(columns=['date'])
    df['month_num']=df['date_time'].dt.month
    df['only_date']=df['date_time'].dt.date
    return df


# main function for given data 

def df_of_comment(url):
    id=extract_video_id(url)    
    comments = get_comments(id)
    df=create_df(comments)
    return df

