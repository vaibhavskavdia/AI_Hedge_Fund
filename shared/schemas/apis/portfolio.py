from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, Field

# ==========================================================
# Portfolio Table Response
# ==========================================================

class PortfolioResponse(BaseModel):
    ticker: str
    prediction_probability: float
    weight: float
    timestamp: datetime


# ==========================================================
# Portfolio Recommendation Response
# ==========================================================

class PortfolioRecommendation(BaseModel):
    ticker: str
    weight: float
    allocation: float
    prediction_probability: float