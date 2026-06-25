from fastapi import APIRouter
from sqlalchemy import text
import pandas as pd

from shared.configs.database import engine

router = APIRouter(
    prefix="/portfolio-intelligence",
    tags=["Portfolio Intelligence"]
)


@router.get("/")
def portfolio_intelligence():

    portfolio = pd.read_sql(
        text("""
        SELECT *
        FROM portfolio_positions
        ORDER BY weight DESC
        """),
        engine
    )

    risk = pd.read_sql(
        text("""
        SELECT *
        FROM portfolio_risk
        """),
        engine
    )

    if portfolio.empty:
        return {
            "message": "No portfolio found"
        }

    total_positions = len(portfolio)

    avg_probability = round(
        portfolio["prediction_score"].mean(),
        4
    )

    total_weight = round(
        portfolio["weight"].sum(),
        4
    )

    sector_breakdown = (
        portfolio.groupby("sector")["weight"]
        .sum()
        .round(4)
        .to_dict()
    )

    avg_risk = None

    if not risk.empty:

        avg_risk = round(
            risk["risk_score"].mean(),
            2
        )

    top_holdings = (
        portfolio[
            [
                "ticker",
                "sector",
                "weight",
                "prediction_score"
            ]
        ]
        .head(10)
        .to_dict(
            orient="records"
        )
    )

    return {

        "portfolio_size": total_positions,

        "total_weight": total_weight,

        "average_prediction_score": avg_probability,

        "average_risk_score": avg_risk,

        "sector_breakdown": sector_breakdown,

        "top_holdings": top_holdings
    }