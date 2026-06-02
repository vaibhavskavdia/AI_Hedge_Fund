import yfinance as yf
from transformers import pipeline
from shared.configs.database import SessionLocal
from sqlalchemy.orm import Session
from shared.schemas.news_sentiment import NewsSentiment

db: Session = SessionLocal()
sentiment_model = pipeline("text-classification",model="ProsusAI/finbert")
ticker = "AAPL"
stock = yf.Ticker(ticker)
news = stock.news
def sentiment_to_score(label, score):

    if label == "positive":
        return score

    elif label == "negative":
        return -score

    return 0.0

for article in news[:10]:

    title = article["content"]["title"]

    result = sentiment_model(title)[0]
    

    numeric_score = sentiment_to_score(result["label"],result["score"])
    news_entry = NewsSentiment(ticker=ticker,headline=title,sentiment=result["label"],score=float(numeric_score))

    db.add(news_entry)
    print("\nHeadline:")
    print(title)

    print("Sentiment:")
    print(result)

db.commit()
db.close()

print("News sentiment stored successfully!")