import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns
from io import BytesIO
import base64
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def plot_comments_per_day(df):
    daily_counts = df['only_date'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily_counts.index, daily_counts.values, marker='o', color='teal')
    ax.set_title("YouTube Comments Per Month")
    ax.set_ylabel("Comment Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def plot_comments_by_weekday(df):
    weekday_counts = df['day'].value_counts()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_counts = weekday_counts.reindex(weekday_order)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette='coolwarm', ax=ax)
    ax.set_title("Comments by Weekday")
    ax.set_xlabel("Day")
    ax.set_ylabel("Comment Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_avg_comment_length_over_time(df):
    df['comment_length'] = df['message'].astype(str).apply(len)
    avg_len = df.groupby('only_date')['comment_length'].mean()
    fig, ax = plt.subplots(figsize=(14, 5))
    avg_len.plot(ax=ax, color='purple', marker='o')
    ax.set_title("Average Comment Length Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Avg. Length")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_weekly_comments(df):
    df['only_date'] = pd.to_datetime(df['only_date'])
    df['week'] = df['only_date'].dt.isocalendar().week
    weekly_counts = df['week'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=weekly_counts.index, y=weekly_counts.values, marker='o', color='blue', ax=ax)
    ax.set_title("Weekly Comment Count")
    ax.set_xlabel("Week Number")
    ax.set_ylabel("Number of Comments")
    plt.tight_layout()
    return fig

def plot_comment_heatmap(df):
    # Ensure date_time is in datetime format
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['hour'] = df['date_time'].dt.hour
    pivot_table = df.pivot_table(index='day', columns='hour', values='message', aggfunc='count').fillna(0)
    
    # Order the weekdays correctly
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(weekday_order)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot_table, cmap='YlGnBu', linewidths=0.5, ax=ax)
    ax.set_title("Heatmap of Comments by Day and Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")
    return fig

# date_time.py or a separate utils.py file
import base64
import io
from matplotlib.figure import Figure 

def fig_to_base64(fig: Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return base64_img


# df=pd.read_csv('comments.csv')

# fig=plot_comment_heatmap(df)

# plt.show()