from pydantic import BaseModel


class PortfolioRecommendation(BaseModel):
    ticker: str
    weight: float
    allocation: float
    prediction_probability: float