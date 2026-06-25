from pydantic import BaseModel
from typing import List


class TopStock(BaseModel):

    ticker: str
    prediction_score: float
    expected_return_5d: float
    risk_score: float
    recommendation: str


class SectorIntelligenceResponse(BaseModel):

    sector: str

    stock_count: int

    average_prediction_score: float

    average_expected_return: float

    average_risk_score: float

    top_stocks: List[TopStock]