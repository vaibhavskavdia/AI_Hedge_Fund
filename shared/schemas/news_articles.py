from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text
)

from shared.configs.base import Base


class NewsArticle(Base):

    __tablename__ = "news_articles"

    id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(
        String,
        nullable=False,
        index=True
    )

    headline = Column(Text)

    summary = Column(Text)

    source = Column(String)

    url = Column(Text)

    published_at = Column(DateTime)

    created_at = Column(DateTime)