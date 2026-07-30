from typing import List, Literal

from pydantic import BaseModel, Field


class PortfolioRequest(BaseModel):
    """
    Request model for AI portfolio generation.
    """

    investment_amount: float = Field(
        ...,
        gt=0,
        description="Total amount to invest.",
        examples=[100000],
    )

    risk_profile: Literal[
        "Conservative",
        "Balanced",
        "Aggressive",
    ] = Field(
        ...,
        description="Investor risk profile.",
    )

    preferred_sectors: List[str] = Field(
        default_factory=list,
        description=(
            "Preferred sectors for portfolio construction. "
            "Leave empty to consider all sectors."
        ),
        examples=[
            [
                "Technology",
                "Healthcare",
            ]
        ],
    )

    max_holdings: int = Field(
        default=10,
        ge=1,
        le=30,
        description="Maximum number of stocks in the portfolio.",
        examples=[10],
    )