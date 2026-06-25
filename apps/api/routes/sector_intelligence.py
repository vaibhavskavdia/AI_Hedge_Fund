from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from shared.configs.database import SessionLocal
from shared.schemas.final_portfolio import FinalPortfolio
from shared.schemas.apis.sector_intelligence import (SectorIntelligenceResponse,TopStock)

router = APIRouter(prefix="/sector-intelligence",tags=["Sector Intelligence"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{sector}",response_model=SectorIntelligenceResponse)

def get_sector_intelligence(sector: str,db: Session = Depends(get_db)):

    stocks = (db.query(FinalPortfolio).filter(func.lower(FinalPortfolio.sector)== sector.lower()).all())

    if len(stocks) == 0:
        raise HTTPException(status_code=404,detail="Sector not found")

    avg_prediction = (sum(x.prediction_score for x in stocks)/ len(stocks))

    avg_return = (sum(x.expected_return_5d for x in stocks)/ len(stocks))

    avg_risk = (sum(x.risk_score for x in stocks)/ len(stocks))

    ranked = sorted(stocks,key=lambda x: x.portfolio_score,reverse=True)[:5]

    top_stocks = []
    for stock in ranked:
        top_stocks.append(
            TopStock(
                ticker=stock.ticker,
                prediction_score=round(stock.prediction_score,4),
                expected_return_5d=round(stock.expected_return_5d,2),
                risk_score=round(stock.risk_score,2),
                recommendation=stock.recommendation))

    return SectorIntelligenceResponse(
        sector=sector,
        stock_count=len(stocks),
        average_prediction_score=round(avg_prediction,4),
        average_expected_return=round(avg_return,2),
        average_risk_score=round(avg_risk,2),
        top_stocks=top_stocks)