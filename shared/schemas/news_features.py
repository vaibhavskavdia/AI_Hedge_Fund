from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from shared.configs.base import Base


class NewsFeature(Base):

    __tablename__ = "news_features"

    id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(
        String,
        index=True
    )

    timestamp = Column(DateTime)

    avg_sentiment_score = Column(Float)

    positive_count = Column(Integer)

    negative_count = Column(Integer)

    neutral_count = Column(Integer)