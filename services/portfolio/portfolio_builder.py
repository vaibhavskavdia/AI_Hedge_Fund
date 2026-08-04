import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.configs.database import engine
from shared.configs.database import SessionLocal
from shared.schemas.portfolio_positions import PortfolioPosition
from shared.constants.sector_mapper import SECTOR_MAP
from logger import logger

QUERY = """
SELECT *
FROM predictions
ORDER BY timestamp DESC;
"""

def build_portfolio():
    logger.info("Loading predictions")
    df = pd.read_sql(text(QUERY), engine)
    logger.info(f"Total prediction rows: {len(df)}")

    df = (
        df.sort_values("timestamp", ascending=False)
        .drop_duplicates(subset=["ticker"], keep="first")
    )

    logger.info(f"Unique tickers: {len(df)}")

    portfolio = df.copy()

    logger.info(f"After probability filter: {len(portfolio)}")

    portfolio["sector"] = portfolio["ticker"].map(SECTOR_MAP)

    logger.info(
        f"Missing sectors: {portfolio['sector'].isna().sum()}"
    )

    portfolio = portfolio.dropna(subset=["sector"])

    logger.info(f"Final portfolio size: {len(portfolio)}")
    # Weighting
    total_prob = (portfolio["prediction_probability"].sum())
    portfolio["weight"] = (portfolio["prediction_probability"]/total_prob)
    
    # Max 20% position cap
    portfolio["weight"] = (portfolio["weight"].clip(upper=0.20))
    portfolio["weight"] = (portfolio["weight"]/portfolio["weight"].sum())
    db: Session = SessionLocal()

    try:
        db.query(PortfolioPosition).delete()
        db.commit()
        for _, row in portfolio.iterrows():
            position = PortfolioPosition(
                ticker=row["ticker"],
                sector=row["sector"],
                prediction_score=float(row["prediction_probability"]),weight=float(row["weight"]))
            db.add(position)
        db.commit()
        logger.info("Portfolio positions stored successfully")
        print(portfolio[["ticker","sector","prediction_probability","weight"]])

    except Exception as e:
        db.rollback()
        logger.error(str(e))
    finally:
        db.close()

if __name__ == "__main__":

    build_portfolio()