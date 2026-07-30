from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    ticker: str
    rating: str
    conviction: str
    position_size: int
    horizon: str
    bull_case: str
    bear_case: str
    recommendation: str