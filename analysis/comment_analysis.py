import pandas as pd
from textblob import TextBlob
import numpy as np

def analyze_comments_sentiment(comments_df):
    """Analyze sentiment in player comments"""
    def get_sentiment(text):
        return TextBlob(str(text)).sentiment.polarity

    sentiments = {
        'sentiment_scores': comments_df['text'].apply(get_sentiment),
        'average_sentiment': comments_df['text'].apply(get_sentiment).mean(),
        'positive_comments': len(comments_df[comments_df['text'].apply(get_sentiment) > 0]),
        'negative_comments': len(comments_df[comments_df['text'].apply(get_sentiment) < 0])
    }
    return sentiments

def extract_comment_topics(comments_df, n_topics=5):
    """Extract main topics from comments using basic keyword analysis"""
    common_words = pd.Series(' '.join(comments_df['text']).lower().split()).value_counts()
    return common_words.head(n_topics).to_dict()