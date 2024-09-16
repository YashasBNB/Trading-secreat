import requests
from config import NEWS_API_KEY, FINNHUB_API_KEY

def fetch_news():
    news_url = f'https://newsapi.org/v2/everything?q=forex&apiKey={NEWS_API_KEY}'
    finnhub_url = f'https://finnhub.io/api/v1/news?category=forex&token={FINNHUB_API_KEY}'
    
    news_response = requests.get(news_url).json()
    finnhub_response = requests.get(finnhub_url).json()
    
    # Ensure the return only contains two items: news articles and a sentiment score
    news_articles = news_response.get("articles", [])
    sentiment_score = analyze_sentiment(news_articles)
    
    return news_articles, sentiment_score

def analyze_sentiment(news_articles):
    from textblob import TextBlob

    sentiment_score = 0.0
    article_count = 0

    for article in news_articles:
        description = article.get('description', '')
        if description:
            analysis = TextBlob(description)
            sentiment_score += analysis.sentiment.polarity
            article_count += 1

    if article_count == 0:
        return 0

    return sentiment_score / article_count
