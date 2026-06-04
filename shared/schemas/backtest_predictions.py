from sqlalchemy import Column, Integer, String, Float, DateTime
from shared.configs.base import Base


class BacktestPrediction(Base):

    __tablename__ = "backtest_predictions"

    id = Column(Integer, primary_key=True)

    ticker = Column(String, index=True)

    timestamp = Column(DateTime, index=True)

    target = Column(Integer)

    prediction_probability = Column(Float)

    predicted_class = Column(Integer)

    fold = Column(Integer)