from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from shared.configs.base import Base


class StockPrice(Base):
    __tablename__ = "stock_prices"

    __table_args__ = (
        UniqueConstraint(
            "ticker",
            "timestamp",
            name="uq_stock_timestamp",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String(10), nullable=False, index=True)

    timestamp = Column(DateTime, nullable=False, index=True)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
   