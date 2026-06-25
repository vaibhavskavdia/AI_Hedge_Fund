from pydantic import BaseModel


class StockIntelligenceResponse(BaseModel):

    ticker: str
    sector: str

    prediction_score: float

    expected_return_5d: float

    risk_score: float
    risk_level: str

    recommendation: str

    avg_sentiment_score: float

    positive_count: int
    negative_count: int
    neutral_count: int