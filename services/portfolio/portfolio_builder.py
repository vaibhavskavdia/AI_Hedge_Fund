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
    # Latest prediction per ticker
    df = (df.sort_values("timestamp",ascending=False).drop_duplicates(subset=["ticker"],keep="first"))

    # Long signals only
    portfolio = df[df["prediction_probability"] >= 0.45].copy()
    if len(portfolio) == 0:
        logger.warning("No long positions generated")
        return

    # Add sector
    portfolio["sector"] = (portfolio["ticker"].map(SECTOR_MAP))
    portfolio = portfolio.dropna(subset=["sector"])

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