from pydantic import BaseModel
from datetime import datetime

class PortfolioResponse(BaseModel):
    ticker: str
    prediction_probability: float
    weight: float
    timestamp: datetime