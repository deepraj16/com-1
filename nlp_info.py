# NLP info with youtube API 
# emoji anylysis with emoji library 
# graphical representation of data 


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import emoji    
import re
import string  
from collections import Counter
from wordcloud import WordCloud
import emoji
from io import BytesIO
import base64
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# i want a conut of word 
# counts of sentance 

def text_stats(df, col='message'):
    all_text = ' '.join(df[col].dropna().astype(str))
    word_count = len(all_text.split())
    sentence_count = len(re.findall(r'[.!?]', all_text))
    return {
        'Total Words': word_count,
        'Total Sentences': sentence_count
    }

def sentmint_bar(df):
    sentiment_counts = df['Sentiment'].value_counts()
    colors = sns.color_palette("Set2")

    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=colors, ax=ax)
    ax.set_title("Sentiment Distribution (Bar Chart)")
    ax.set_ylabel("Count")
    ax.set_xlabel("Sentiment")
    
    return fig

def sentmint_grph(df):
    sentiment_counts = df['Sentiment'].value_counts()
    colors = sns.color_palette("pastel")[0:len(sentiment_counts)]
    
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
           colors=colors, startangle=140, shadow=True)
    ax.set_title("Sentiment Distribution (Pie Chart)")
    
    return fig

def common_word(df,col='message'): 
    words =[]
    f= open('hindlish_stopword.txt','r')
    stop_word=f.read().split('\n')
    marathi_stopword =['ahe','la','te','ha','kare','mi']
    for message1 in df['message']: 
        for word in message1.lower().split():
            if word not in stop_word:
                if word not in marathi_stopword:
                    words.append(word)    
    cleaned_list = [item for item in words if re.match(r'^[a-zA-Z\s]+$', item)]
    return cleaned_list


def mostcommn_word(df):
    cleaned_list = common_word(df)  # Assuming this returns a list of cleaned words
    word_counts = Counter(cleaned_list).most_common(20)
    df_bigrams = pd.DataFrame(word_counts, columns=['Word', 'Frequency'])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Frequency', y='Word', data=df_bigrams, palette='Blues_r', ax=ax)
    ax.set_title('Top 20 Most Common Words in Comments')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Words')

    return fig


def make_word_cloud(df):
    cleaned_list = common_word(df)  
    text = ' '.join(cleaned_list)
    
    wordcloud = WordCloud(width=1000, height=1000, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # hide axes
    ax.set_title("Word Cloud of Comments")
    return fig


def make_bigram(df): 
    cleaned_words = common_word(df)  # Assuming common_word function returns a list of words
    bigrams = list(zip(cleaned_words, cleaned_words[1:]))  # Create bigrams

    bigram_strings = [' '.join(bigram) for bigram in bigrams]

    bigram_counts = Counter(bigram_strings)
    df_bigrams = pd.DataFrame(bigram_counts.most_common(10), columns=['Bigram', 'Count'])

    # Create bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Count', y='Bigram', data=df_bigrams, palette='viridis')
    ax.set_title("Top 10 Most Common Bigrams")
    
    return fig

def make_emoji(df): 
    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).head(10)

def show_comments(df):
    top_good = df[df['Sentiment'] == 'Good'].head(5)[['message', 'Sentiment']]
    top_bad = df[df['Sentiment'] == 'Bad'].head(5)[['message', 'Sentiment']]
    return top_good, top_bad

def show_comments1(df):
    top_good = df[df['Sentiment'] == 'Good'].head(5)[['message', 'Sentiment']]
    top_bad = df[df['Sentiment'] == 'Bad'].head(5)[['message', 'Sentiment']]
    
    result = {
        'Top_Good_Comments': top_good.to_dict(orient='records'),
        'Top_Bad_Comments': top_bad.to_dict(orient='records')
    }
    return result

def make_emoji_graph(df):
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])

    emoji_counts = Counter(emojis).most_common(10)
    labels, values = zip(*emoji_counts)

    fig, ax = plt.subplots()
    ax.bar(labels, values, color='skyblue')
    ax.set_title('Top Emojis')
    return fig
def make_emoji_graph1(df):
    emojis = []
    for msg in df['message']:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    
    # Count and get top 10 emojis
    emoji_counts = Counter(emojis).most_common(10)
    if not emoji_counts:
        print("No emojis found.")
        return None

    labels, values = zip(*emoji_counts)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, values, color='lightsalmon', edgecolor='black')

    # Add text labels on top of each bar
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value),
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_title('Top 10 Most Used Emojis', fontsize=16, fontweight='bold')
    ax.set_xlabel('Emojis', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.spines[['right', 'top']].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64



# top_good, top_bad = show_comments(df)
# print("Top 5 Good Comments:")
# print(top_bad,top_good)
# df=pd.read_csv('comments2.csv')
# print(show_comments1(df))