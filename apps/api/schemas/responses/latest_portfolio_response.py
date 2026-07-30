from pydantic import BaseModel
from typing import Any


class LatestPortfolioResponse(BaseModel):
    portfolio_id: int
    portfolio: dict[str, float]
    recommendations: list[dict[str, Any]]
    committee_review: dict[str, Any]