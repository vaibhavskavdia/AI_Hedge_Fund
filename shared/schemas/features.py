from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from shared.configs.base import Base


class FeatureStore(Base):

    __tablename__ = "feature_store"

    id = Column(Integer, primary_key=True)

    ticker = Column(String, index=True)

    timestamp = Column(DateTime)

    returns = Column(Float)

    sma_10 = Column(Float)

    ema_10 = Column(Float)

    volatility_10 = Column(Float)

    lag_1 = Column(Float)

    lag_2 = Column(Float)

    target = Column(Integer)