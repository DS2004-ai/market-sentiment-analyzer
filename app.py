# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go  # Using your preferred library

# Import your functions from Phase 1
from sentiment_analyzer import get_stock_data, get_news_headlines, analyze_sentiment, process_and_merge_data

# --- Reusable Charting Function (using your code) ---
def create_sentiment_chart(df, ticker_symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Stock Price', yaxis='y1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['mean_sentiment'], name='Sentiment Score', yaxis='y2', line=dict(color='red')))
    fig.update_layout(
        title_text=f"{ticker_symbol} Price vs. News Sentiment",
        xaxis=dict(title='Date'),
        yaxis=dict(title='Stock Price', side='left'),
        yaxis2=dict(title='Average Sentiment', overlaying='y', side='right', range=[-1, 1]),
        legend=dict(x=0.01, y=0.99)
    )
    return fig

# --- Streamlit App Layout ---
st.title("Market Sentiment Analyzer 📈")
st.sidebar.header("User Input")

ticker_symbol = st.sidebar.text_input("Enter a Stock Ticker", "AAPL").upper()
search_term = st.sidebar.text_input("Enter a Search Term for News", "Apple Inc")

if st.sidebar.button("Analyze Sentiment"):
    with st.spinner(f"Fetching data and analyzing sentiment for {ticker_symbol}..."):
        try:
            # Run the same logic as your notebook test
            stock_data = get_stock_data(ticker_symbol, "3mo")
            news_data = get_news_headlines(search_term)
            
            if stock_data.empty or news_data.empty:
                st.error("Could not retrieve data. Please check the ticker or search term.")
            else:
                news_with_sentiment = analyze_sentiment(news_data)
                combined_data = process_and_merge_data(stock_data, news_with_sentiment)

                # --- Display everything using Streamlit commands ---
                st.header(f"Analysis for {ticker_symbol}")

                final_chart = create_sentiment_chart(combined_data, ticker_symbol)
                st.plotly_chart(final_chart, use_container_width=True)
                
                st.subheader("Sentiment Signal")
                latest_sentiment = combined_data['mean_sentiment'].iloc[-1]
                if latest_sentiment > 0.2:
                    st.success(f"Signal: Strong Positive Sentiment ({latest_sentiment:.2f})")
                elif latest_sentiment < -0.2:
                    st.error(f"Signal: Strong Negative Sentiment ({latest_sentiment:.2f})")
                else:
                    st.warning(f"Signal: Neutral Sentiment ({latest_sentiment:.2f})")

                st.subheader("Recent News Headlines")
                st.dataframe(news_with_sentiment[['title', 'sentiment']])

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Enter a ticker and search term, then click 'Analyze Sentiment'.")