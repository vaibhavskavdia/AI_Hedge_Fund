from typing import Any

from pydantic import BaseModel


class PortfolioIntelligenceResponse(BaseModel):
    portfolio_id: int
    recommendations: list[dict[str, Any]]

    summary: str | None = None
    strengths: list[str] = []
    weaknesses: list[str] = []
    opportunities: list[str] = []
    risks: list[str] = []

    model_config = {
        "extra": "allow",
    }