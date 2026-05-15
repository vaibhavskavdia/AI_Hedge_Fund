from sqlalchemy import Column, Integer, String, Float, DateTime
from shared.configs.base import Base

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True)

    timestamp = Column(DateTime)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    volume = Column(Float)