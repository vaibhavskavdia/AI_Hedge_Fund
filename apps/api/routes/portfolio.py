from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from shared.configs.database import SessionLocal
from shared.schemas.portfolio_positions import PortfolioPosition
from shared.schemas.features import FeatureStore
from shared.schemas.apis.portfolio import PortfolioResponse
from apps.api.schemas.recommendation import PortfolioRecommendation
from agents.portfolio_manager import PortfolioManager
from agents.portfolio_construction_agent import PortfolioConstructionAgent
from services.risk.risk_engine import RiskEngine
import threading
from services.jobs.job_manager import (create_job,get_job,)
from services.portfolio.portfolio_repository import save_portfolio, get_latest_portfolio
from services.dashboard.dashboard_builder import DashboardBuilder
dashboard_builder = DashboardBuilder()
risk_engine = RiskEngine()
router = APIRouter(prefix="/portfolio",tags=["Portfolio"])

portfolio_manager = PortfolioManager()
portfolio_constructor = (PortfolioConstructionAgent())

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/",response_model=list[PortfolioResponse])

def get_portfolio(db: Session = Depends(get_db)):

    latest_timestamp = (db.query(PortfolioPosition.timestamp).order_by(PortfolioPosition.timestamp.desc()).first())

    if not latest_timestamp:
        return []

    portfolio = (db.query(PortfolioPosition).filter(PortfolioPosition.timestamp == latest_timestamp[0]).all())

    return portfolio


@router.get("/recommend",response_model=list[PortfolioRecommendation])

def recommend_portfolio(
    investment_amount: float = Query(..., gt=0),top_n: int = Query(5, gt=0),
    risk_profile: str = Query("moderate"),db: Session = Depends(get_db)):

    latest_timestamp = (db.query(PortfolioPosition.timestamp).order_by(PortfolioPosition.timestamp.desc()).first())

    if not latest_timestamp:
        return []

    positions = (db.query(PortfolioPosition).filter(PortfolioPosition.timestamp == latest_timestamp[0]).all())

    portfolio_data = []

    for position in positions:

        feature = (db.query(FeatureStore).filter(FeatureStore.ticker == position.ticker)
                   .order_by(FeatureStore.timestamp.desc()).first())

        if not feature:
            continue

        risk_result = risk_engine.evaluate_position(feature)

        risk_score = risk_result["risk_score"]

        portfolio_data.append({"position": position,"risk_score": risk_score})

    if risk_profile.lower() == "conservative":

        portfolio_data = sorted(portfolio_data,key=lambda x: x["risk_score"])

    elif risk_profile.lower() == "aggressive":

        portfolio_data = sorted(portfolio_data,
            key=lambda x: (x["position"].prediction_probability- x["risk_score"] * 0.001),reverse=True)

    else:

        portfolio_data = sorted(
            portfolio_data,
            key=lambda x: (x["position"].prediction_probability- x["risk_score"] * 0.005),reverse=True)

    portfolio_data = portfolio_data[:top_n]

    positions = [item["position"] for item in portfolio_data]

    if len(positions) == 0:
        return []

    total_weight = sum(p.weight for p in positions)

    recommendations = []

    for position in positions:

        normalized_weight = (position.weight / total_weight)

        allocation = (normalized_weight* investment_amount)

        recommendations.append(
            PortfolioRecommendation(
                ticker=position.ticker,
                weight=round(normalized_weight,4),
                allocation=round(allocation,2),
                prediction_probability=round(position.prediction_probability,4)))

    return recommendations

@router.post("/ai-recommendation")

def ai_recommendation(payload: dict):

    ticker = payload["ticker"]

    result = portfolio_manager.recommend(ticker=ticker)

    return result

@router.post("/ai-portfolio")
def ai_portfolio(payload: dict):

    tickers = payload["tickers"]

    job_id = create_job()

    threading.Thread(
        target=dashboard_builder.build_dashboard,
        args=(tickers, job_id),
        daemon=True,
    ).start()

    return {
        "job_id": job_id
    }

@router.get("/latest")
def latest_portfolio():

    portfolio = get_latest_portfolio()

    if portfolio is None:
        return {"error": "No portfolio found"}

    return {
        "portfolio_id": portfolio.id,
        "portfolio": portfolio.portfolio,
        "recommendations": portfolio.recommendations,
        "committee_review": portfolio.committee_review
    }

portfolio_manager = PortfolioManager()

@router.get("/portfolio-intelligence")
def portfolio_intelligence():

    portfolio = get_latest_portfolio()

    if portfolio is None:
        return {
            "error": "No portfolio found"
        }

    if portfolio.portfolio_intelligence is None:
        return {
            "error": "Portfolio intelligence not generated."
        }

    analysis = dict(portfolio.portfolio_intelligence)

    analysis["portfolio_id"] = portfolio.id
    analysis["recommendations"] = portfolio.recommendations

    return analysis

@router.get("/job/{job_id}")
def job_status(job_id: str):

    job = get_job(job_id)

    if job is None:
        return {
            "error": "Job not found"
        }

    return job