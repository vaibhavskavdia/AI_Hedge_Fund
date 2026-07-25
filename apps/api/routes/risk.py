from fastapi import APIRouter

from services.portfolio.portfolio_repository import (
    get_latest_portfolio
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


@router.get("/latest")
def latest_risk():

    portfolio_run = get_latest_portfolio()

    if portfolio_run is None:
        return {
            "error": "No portfolio found"
        }

    if portfolio_run.risk_analysis is None:
        return {
            "error": "Risk analysis has not been generated."
        }

    risk = dict(portfolio_run.risk_analysis)

    risk["portfolio_id"] = portfolio_run.id
    risk["portfolio"] = portfolio_run.portfolio

    return risk