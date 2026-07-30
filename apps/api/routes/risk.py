from fastapi import APIRouter, HTTPException
from apps.api.schemas.responses.risk_response import RiskResponse
from services.portfolio.portfolio_repository import (
    get_latest_portfolio
)

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


@router.get(
    "/latest",
    summary="Get latest portfolio risk analysis",
    description="Returns the AI-generated risk analysis for the latest portfolio.",
    response_model=RiskResponse,
    status_code=200,
)
def latest_risk():

    portfolio_run = get_latest_portfolio()

    if portfolio_run is None:
        raise HTTPException(
    status_code=404,
    detail="No portfolio found.",)

    if portfolio_run.risk_analysis is None:
        raise HTTPException(
    status_code=404,
    detail="Risk analysis has not been generated.",)

    risk = {
    **portfolio_run.risk_analysis,
    "portfolio_id": portfolio_run.id,
    "portfolio": portfolio_run.portfolio,}

    return RiskResponse(**risk)