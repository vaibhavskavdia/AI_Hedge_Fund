from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)
from datetime import datetime
from shared.configs.base import Base

class PortfolioPosition(Base):

    __tablename__ = "portfolio_positions"

    id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(String)

    sector = Column(String)

    weight = Column(Float)

    prediction_score = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )