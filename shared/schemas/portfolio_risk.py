from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from shared.configs.base import Base


class PortfolioRisk(Base):

    __tablename__ = "portfolio_risk"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)

    risk_score = Column(Float)

    risk_level = Column(String)

    max_position_size = Column(Float)

    stop_loss_percent = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )