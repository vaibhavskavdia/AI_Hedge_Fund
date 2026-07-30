from pydantic import BaseModel


class RiskResponse(BaseModel):
    portfolio_id: int

    portfolio: dict[str, float]

    largest_holding: str | None

    largest_weight: float

    concentration_risk: str

    risk_score: float