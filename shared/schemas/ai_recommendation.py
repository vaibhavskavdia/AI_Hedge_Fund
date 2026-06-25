from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from shared.configs.base import Base


class AIRecommendation(Base):

    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True, nullable=False)

    rating = Column(String)

    conviction = Column(String)

    position_size = Column(Integer)

    horizon = Column(String)

    bull_case = Column(Text)

    bear_case = Column(Text)

    recommendation = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )