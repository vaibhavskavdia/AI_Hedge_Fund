import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.configs.database import engine
from shared.configs.database import SessionLocal
from shared.schemas.portfolio_positions import PortfolioPosition
from logger import logger


QUERY = """
SELECT *
FROM predictions
ORDER BY timestamp DESC;
"""


def build_portfolio():

    logger.info("Loading predictions")

    df = pd.read_sql(text(QUERY),engine)

    # Latest prediction per ticker

    df = (df.sort_values("timestamp", ascending=False).drop_duplicates(subset=["ticker"],keep="first"))

    # Long signals only

    portfolio = df[df["prediction_probability"] >= 0.53].copy()
    total_prob = portfolio["prediction_probability"].sum()

    portfolio["weight"] = (portfolio["prediction_probability"]/ total_prob)

    if len(portfolio) == 0:
        logger.warning("No long positions generated")
        return
    # Position cap

    if len(portfolio) > 5:
        portfolio["weight"] = portfolio["weight"].clip(upper=0.20)
        portfolio["weight"] = portfolio["weight"] / portfolio["weight"].sum()

    db: Session = SessionLocal()

    try:

        for _, row in portfolio.iterrows():

            position = PortfolioPosition(ticker=row["ticker"],prediction_probability=float(row["prediction_probability"]),
                                         weight=float(row["weight"]),timestamp=row["timestamp"])
            db.add(position)

        db.commit()

        logger.info("Portfolio positions stored successfully")

    except Exception as e:

        db.rollback()

        logger.error(str(e))

    finally:

        db.close()


if __name__ == "__main__":

    build_portfolio()