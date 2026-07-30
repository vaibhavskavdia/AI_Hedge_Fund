from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from shared.configs.database import SessionLocal

from shared.schemas.apis.portfolio import (
    PortfolioResponse,
    PortfolioRecommendation,
)

from shared.schemas.portfolio_positions import PortfolioPosition

from apps.api.schemas.requests.portfolio_request import PortfolioRequest
from apps.api.schemas.requests.recommendation_request import RecommendationRequest

from apps.api.schemas.responses.job_status_response import JobStatusResponse
from apps.api.schemas.responses.latest_portfolio_response import (
    LatestPortfolioResponse,
)
from apps.api.schemas.responses.portfolio_intelligence_response import (
    PortfolioIntelligenceResponse,
)
from apps.api.schemas.responses.recommendation_response import (
    RecommendationResponse,
)

from services.portfolio.portfolio_service import PortfolioService
from services.portfolio.recommendation_service import RecommendationService
from services.portfolio.portfolio_repository import get_latest_portfolio
from services.jobs.job_manager import get_job

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)

recommendation_service = RecommendationService()
portfolio_service = PortfolioService()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    summary="Get latest portfolio positions",
    description="Returns the latest generated portfolio positions.",
    response_model=list[PortfolioResponse],
    status_code=200,
)
def get_portfolio(db: Session = Depends(get_db)):

    latest_timestamp = (
        db.query(PortfolioPosition.timestamp)
        .order_by(PortfolioPosition.timestamp.desc())
        .first()
    )

    if not latest_timestamp:
        return []

    portfolio = (
        db.query(PortfolioPosition)
        .filter(
            PortfolioPosition.timestamp == latest_timestamp[0]
        )
        .all()
    )

    return portfolio


@router.get(
    "/recommend",
    summary="Generate portfolio recommendations",
    description="Returns portfolio recommendations based on investment amount and risk profile.",
    response_model=list[PortfolioRecommendation],
    status_code=200,
)
def recommend_portfolio(
    investment_amount: float = Query(..., gt=0),
    top_n: int = Query(5, gt=0),
    risk_profile: str = Query("moderate"),
    db: Session = Depends(get_db),
):

    return recommendation_service.recommend(
        db=db,
        investment_amount=investment_amount,
        top_n=top_n,
        risk_profile=risk_profile,
    )


@router.post(
    "/ai-recommendation",
    summary="Generate AI stock recommendation",
    description="Returns an AI-generated recommendation for a single stock.",
    response_model=RecommendationResponse,
    status_code=200,
)
def ai_recommendation(
    request: RecommendationRequest,
):

    return recommendation_service.ai_recommendation(
        request.ticker,
    )


@router.post(
    "/ai-portfolio",
    summary="Generate AI portfolio",
    description="Starts asynchronous AI portfolio generation.",
    response_model=JobStatusResponse,
    status_code=202,
)
def ai_portfolio(
    request: PortfolioRequest,
):
    return portfolio_service.generate(request)


@router.get(
    "/latest",
    summary="Get latest AI portfolio",
    description="Returns the latest generated portfolio.",
    response_model=LatestPortfolioResponse,
    status_code=200,
)
def latest_portfolio():

    portfolio = get_latest_portfolio()

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="No portfolio found",
        )

    return LatestPortfolioResponse(
        portfolio_id=portfolio.id,
        portfolio=portfolio.portfolio,
        recommendations=portfolio.recommendations,
        committee_review=portfolio.committee_review,
    )


@router.get(
    "/portfolio-intelligence",
    summary="Get portfolio intelligence",
    description="Returns AI-generated analysis of the latest portfolio.",
    response_model=PortfolioIntelligenceResponse,
    status_code=200,
)
def portfolio_intelligence():

    portfolio = get_latest_portfolio()

    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="No portfolio found",
        )

    if portfolio.portfolio_intelligence is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio intelligence not generated.",
        )

    analysis = {
        **portfolio.portfolio_intelligence,
        "portfolio_id": portfolio.id,
        "recommendations": portfolio.recommendations,
    }

    return PortfolioIntelligenceResponse(**analysis)


@router.get(
    "/job/{job_id}",
    summary="Get portfolio generation job",
    description="Returns the current status of a portfolio generation job.",
    response_model=JobStatusResponse,
    status_code=200,
)
def job_status(job_id: str):

    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return JobStatusResponse(
    job_id=job_id,
    status=job["status"],
    progress=job.get("progress"),
    step=job.get("step"),
    portfolio_id=job.get("portfolio_id"),
    error=job.get("error"),
)