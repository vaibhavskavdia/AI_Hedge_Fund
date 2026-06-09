from transformers import pipeline
from shared.configs.database import SessionLocal
from shared.schemas.news_articles import NewsArticle
from shared.schemas.news_sentiment import NewsSentiment
from logger import logger

sentiment_model = pipeline("text-classification",model="ProsusAI/finbert")
def generate_news_sentiment():

    logger.info("Generating sentiment scores")
    db = SessionLocal()
    articles = (db.query(NewsArticle).all())
    total_processed = 0
    for article in articles:
        try:
            if not article.headline:
                continue
            result = sentiment_model(article.headline)[0]
            sentiment = result["label"]
            score = float(result["score"])
            sentiment_row = NewsSentiment(ticker=article.ticker,timestamp=article.created_at,headline=article.headline,sentiment=sentiment,score=score)
            db.add(sentiment_row)
            total_processed += 1
        except Exception as e:
            logger.error(f"{article.id}: {e}")
    db.commit()
    db.close()
    logger.info(f"Processed {total_processed} articles")
if __name__ == "__main__":

    generate_news_sentiment()