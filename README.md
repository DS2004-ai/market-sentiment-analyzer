# 📊 Market Sentiment Analyzer

Analyze stock price trends alongside news sentiment to generate a trading signal — all in one dashboard.

## 🚀 Live App

👉 [Try it here](https://market-sentiment-analyzer.streamlit.app/)

---

## 📌 Project Description

**Market Sentiment Analyzer** is a data science dashboard that combines financial data with sentiment analysis to provide insights into how public news sentiment correlates with stock performance.

It:

- Pulls stock prices using `yfinance`
- Scrapes recent news using the NewsAPI
- Analyzes news sentiment using VADER
- Visualizes stock price vs. sentiment in an interactive Plotly chart
- Generates a signal (Positive, Negative, Neutral) based on recent sentiment

---

## 📂 Tech Stack

- **Python**
- **Streamlit** – for the interactive web dashboard
- **YFinance** – to fetch stock price data
- **NewsAPI** – for retrieving relevant news articles
- **VADER Sentiment** – for sentiment analysis
- **Pandas** & **Plotly** – for data manipulation and visualization

---

## 💡 How It Works

1. User enters a **stock ticker** (e.g., `AAPL`) and a **search term** (e.g., "Apple Inc").
2. The app:
   - Fetches 3 months of stock prices
   - Retrieves matching news headlines
   - Scores each headline's sentiment
   - Merges the sentiment scores with stock data
   - Displays both on a dual-axis chart
3. Finally, a signal is displayed based on the average sentiment of the most recent articles.

---

## 🧠 Use Case

This tool is ideal for:

- Retail investors wanting an edge
- Financial analysts interested in alternative data
- Students or researchers exploring **NLP in finance**

---

## 📸 Screenshot

![Market Sentiment Analyzer Screenshot](https://your-screenshot-url-if-any)

---

## 👤 Author

**Roderick Mireku**  
GitHub: [DS2004-ai](https://github.com/DS2004-ai)

---

## 📬 Contact

If you’d like to connect, feel free to [message me on GitHub](https://github.com/DS2004-ai).

---

## ✅ Future Improvements

- Allow time window selection (e.g., 1w, 1mo, 6mo)
- Include more news sources
- Add backtesting feature
- Improve signal generation with machine learning

---

## ⭐️ Give it a Star

If you find this project useful, give it a ⭐️ on GitHub to support it!

