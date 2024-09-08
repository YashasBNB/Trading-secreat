# news_fetcher.py
import requests
from config import NEWS_API_KEY, FINNHUB_API_KEY
from textblob import TextBlob

def fetch_news():
    news_url = f'https://newsapi.org/v2/everything?q=forex&apiKey={NEWS_API_KEY}'
    finnhub_url = f'https://finnhub.io/api/v1/news?category=forex&token={FINNHUB_API_KEY}'
    
    news_response = requests.get(news_url).json()
    finnhub_response = requests.get(finnhub_url).json()
    
    return news_response, finnhub_response

def analyze_sentiment(news_data):
    sentiment_score = 0
    for article in news_data['articles']:
        title = article['title']
        description = article['description']
        analysis = TextBlob(f"{title} {description}")
        sentiment_score += analysis.sentiment.polarity
    
    # Average sentiment score
    sentiment_score = sentiment_score / len(news_data['articles'])
    
    # Return sentiment (Positive: Bullish, Negative: Bearish)
    return "bullish" if sentiment_score > 0 else "bearish"

if __name__ == "__main__":
    news_data, finnhub_data = fetch_news()
    
    # Print the fetched data for review
    print("NewsAPI Data:", news_data)
    print("Finnhub Data:", finnhub_data)
    
    # Analyze and print sentiment
    sentiment = analyze_sentiment(news_data)
    print("Market Sentiment:", sentiment)
