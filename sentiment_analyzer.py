import os
import pandas as pd
import yfinance as yf
from newsapi import NewsApiClient # This should now work correctly
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px # Great for interactive plots in a notebook

# Initialize the NewsAPI client
# Make sure your NEWS_API_KEY environment variable is set!
api_key = os.environ.get('NEWS_API_KEY')
newsapi = NewsApiClient(api_key=api_key)

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

print("Setup Complete!")

# Cell 2: Fetch Stock Data

ticker_symbol = 'TSLA'
stock_df = yf.Ticker(ticker_symbol).history(period='3mo')

# Clean up the index for merging later
stock_df.index = stock_df.index.date
stock_df.index.name = 'date'

print(f"Successfully fetched stock data for {ticker_symbol}.")
stock_df.head() # Display the first 5 rows

# Cell 3: Fetch News Headlines

search_query = 'Tesla Inc'
all_articles = newsapi.get_everything(
    q=search_query,
    language='en',
    sort_by='publishedAt',
    page_size=100
)

# Convert to a DataFrame
news_df = pd.DataFrame(all_articles['articles'])

# Keep only the columns we need
if not news_df.empty:
    news_df = news_df[['publishedAt', 'title']]

print(f"Found {len(news_df)} articles for '{search_query}'.")
news_df.head()

# Cell 4: Analyze Sentiment

# Apply the sentiment analyzer to the 'title' column
# The 'compound' score is what we'll use: a single value from -1 to +1
news_df['sentiment'] = news_df['title'].apply(lambda title: analyzer.polarity_scores(title)['compound'])

# Let's look at the headlines with the most positive and negative sentiment
print("Most Positive Headlines:")
print(news_df.sort_values('sentiment', ascending=False).head())

print("\nMost Negative Headlines:")
print(news_df.sort_values('sentiment', ascending=True).head())

# Cell 5: Process and Merge Data

# 1. Convert 'publishedAt' to just a date
news_df['date'] = pd.to_datetime(news_df['publishedAt']).dt.date

# 2. Group by date and calculate the average sentiment
daily_sentiment_df = news_df.groupby('date')['sentiment'].mean().to_frame('mean_sentiment')

# 3. Join the sentiment data with the stock data
merged_df = stock_df.join(daily_sentiment_df)

# 4. Fill any missing sentiment values (for trading days with no news) with 0
merged_df['mean_sentiment'] = merged_df['mean_sentiment'].fillna(0)

print("Successfully merged stock and sentiment data.")
merged_df.tail(10) # Show the last 10 days of our final dataset

import plotly.graph_objects as go

# Create the figure
fig = go.Figure()

# Add stock price trace (left y-axis)
fig.add_trace(go.Scatter(
    x=merged_df.index,
    y=merged_df['Close'],
    name='Stock Price',
    yaxis='y1',
    line=dict(color='blue')
))

# Add sentiment score trace (right y-axis)
fig.add_trace(go.Scatter(
    x=merged_df.index,
    y=merged_df['mean_sentiment'],
    name='Sentiment Score',
    yaxis='y2',
    line=dict(color='red')
))

# Update layout with dual y-axes
fig.update_layout(
    title=f"{ticker_symbol} Price vs. News Sentiment",
    xaxis=dict(title='Date'),
    yaxis=dict(
        title='Stock Price',
        side='left'
    ),
    yaxis2=dict(
        title='Average Sentiment',
        overlaying='y',
        side='right',
        range=[-1, 1]
    ),
    legend=dict(x=0.01, y=0.99)
)

fig.show()

