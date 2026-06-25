from fastapi import APIRouter

from services.portfolio.portfolio_repository import (
    get_latest_portfolio
)

from agents.portfolio_manager import (
    PortfolioManager
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)

manager = PortfolioManager()


@router.get("/latest")
def latest_risk():

    portfolio_run = (
        get_latest_portfolio()
    )

    if portfolio_run is None:

        return {
            "error":
            "No portfolio found"
        }

    analysis = manager.analyze_portfolio(
        portfolio=portfolio_run.portfolio
    )

    return {

        "portfolio_id":
            portfolio_run.id,

        "portfolio":
            portfolio_run.portfolio,

        "health_score":
            analysis["health_score"],

        "risk_score":
            analysis["risk_score"],

        "diversification":
            analysis["diversification"],

        "diversification_score":
            analysis["diversification_score"],

        "largest_holding":
            analysis["largest_holding"],

        "largest_weight":
            analysis["largest_weight"],

        "largest_sector":
            analysis["largest_sector"],

        "largest_sector_weight":
            analysis["largest_sector_weight"],

        "sector_exposure":
            analysis["sector_exposure"],

        "rebalance_action":
            analysis["rebalance_action"],

        "manager_commentary":
            analysis["manager_commentary"],

        "recommendations":
            analysis["recommendations"]
    }