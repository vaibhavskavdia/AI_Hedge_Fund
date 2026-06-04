from sqlalchemy import Column, Integer, String, Float, DateTime

from shared.configs.base import Base


class PortfolioPosition(Base):

    __tablename__ = "portfolio_positions"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)

    prediction_probability = Column(Float)

    weight = Column(Float)

    timestamp = Column(DateTime)