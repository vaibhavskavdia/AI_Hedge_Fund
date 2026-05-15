from sqlalchemy import Column, Integer, String, Float, DateTime, Text

from shared.configs.base import Base


class NewsArticle(Base):

    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True)

    headline = Column(String)

    content = Column(Text)

    source = Column(String)

    published_at = Column(DateTime)

    sentiment_score = Column(Float)