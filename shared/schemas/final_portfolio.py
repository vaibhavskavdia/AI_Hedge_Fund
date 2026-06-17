from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime

from shared.configs.base import Base


class FinalPortfolio(Base):

    __tablename__ = "final_portfolio"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)

    sector = Column(String)

    prediction_score = Column(Float)

    risk_score = Column(Float)

    portfolio_weight = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )