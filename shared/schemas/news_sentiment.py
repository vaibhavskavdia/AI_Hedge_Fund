from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from shared.configs.base import Base


class NewsSentiment(Base):

    __tablename__ = "news_sentiment"

    id = Column(Integer, primary_key=True)

    ticker = Column(String, nullable=False)

    timestamp = Column(DateTime)

    headline = Column(String)

    sentiment = Column(String)

    score = Column(Float)