from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    JSON,
    String
)

from datetime import datetime

from shared.configs.base import Base


class PortfolioRun(Base):

    __tablename__ = "portfolio_runs"

    id = Column(Integer,primary_key=True)

    created_at = Column(DateTime,default=datetime.utcnow)

    portfolio_name = Column(String,nullable=True)

    portfolio = Column(JSON,nullable=False)

    recommendations = Column(JSON,nullable=False)

    committee_review = Column(JSON,nullable=False)