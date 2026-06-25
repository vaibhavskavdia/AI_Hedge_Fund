from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.configs.database import SessionLocal
from shared.schemas.final_portfolio import FinalPortfolio
from shared.schemas.news_features import NewsFeature
from shared.schemas.apis.stock_intelligence import StockIntelligenceResponse

router = APIRouter(prefix="/stock-intelligence",tags=["Stock Intelligence"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{ticker}",response_model=StockIntelligenceResponse)

def get_stock_intelligence(ticker: str,db: Session = Depends(get_db)):

    stock = (db.query(FinalPortfolio).filter(FinalPortfolio.ticker == ticker.upper()).first())
    if not stock:
        raise HTTPException(status_code=404,detail="Ticker not found")

    news = (db.query(NewsFeature).filter(NewsFeature.ticker == ticker.upper()).first())
    return StockIntelligenceResponse(
        ticker=stock.ticker,
        sector=stock.sector,
        prediction_score=round(stock.prediction_score,4),
        expected_return_5d=round(stock.expected_return_5d,2),
        risk_score=round(stock.risk_score,2),
        risk_level=stock.risk_level,
        recommendation=stock.recommendation,
        avg_sentiment_score=(round(news.avg_sentiment_score, 4)if news else 0),
        positive_count=(news.positive_count if news else 0),
        negative_count=(news.negative_count if news else 0),
        neutral_count=(news.neutral_count if news else 0))