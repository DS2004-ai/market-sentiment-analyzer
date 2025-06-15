import os
import pandas as pd
import yfinance as yf
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_stock_data(ticker_symbol, period='1y'):
    """
    Fetches historical stock data for a given ticker.
    """
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)
    df.index = df.index.date
    df.index.name = 'date'
    return df

def get_news_headlines(query):
    """
    Fetches news headlines for a given query using NewsAPI.
    """
    try:
        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            raise ValueError("NEWS_API_KEY secret not found.")
        newsapi = NewsApiClient(api_key=api_key)
    except Exception as e:
        print(f"Error initializing NewsAPI: {e}")
        return pd.DataFrame()

    all_articles = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='publishedAt',
        page_size=100
    )
    
    articles_df = pd.DataFrame(all_articles['articles'])
    
    if not articles_df.empty:
        articles_df = articles_df[['publishedAt', 'title']]
    
    return articles_df

def analyze_sentiment(df):
    """
    Analyzes the sentiment of each news headline in a DataFrame.
    """
    if 'title' not in df.columns:
        return df
        
    analyzer = SentimentIntensityAnalyzer()
    df['sentiment'] = df['title'].apply(lambda title: analyzer.polarity_scores(title)['compound'])
    return df

def process_and_merge_data(stock_df, news_df):
    """
    Processes and merges the stock and sentiment dataframes.
    """
    if news_df.empty:
        stock_df['mean_sentiment'] = 0
        return stock_df

    news_df['date'] = pd.to_datetime(news_df['publishedAt']).dt.date
    
    daily_sentiment = news_df.groupby('date')['sentiment'].mean().to_frame('mean_sentiment')
    
    merged_df = stock_df.join(daily_sentiment)
    merged_df['mean_sentiment'] = merged_df['mean_sentiment'].fillna(0)
    
    return merged_df

