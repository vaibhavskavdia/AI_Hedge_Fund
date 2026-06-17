from datetime import datetime

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from logger import logger
from shared.configs.database import engine
from shared.configs.database import SessionLocal

from shared.schemas.portfolio_positions import PortfolioPosition
from shared.schemas.portfolio_risk import PortfolioRisk
from shared.schemas.final_portfolio import FinalPortfolio


POSITIONS_QUERY = """
SELECT *
FROM portfolio_positions;
"""

RISK_QUERY = """
SELECT *
FROM portfolio_risk;
"""


def build_final_portfolio():

    logger.info("Loading portfolio positions")

    positions = pd.read_sql(
        text(POSITIONS_QUERY),
        engine
    )

    logger.info("Loading risk data")

    risk = pd.read_sql(
        text(RISK_QUERY),
        engine
    )

    if positions.empty:
        logger.warning(
            "No portfolio positions found"
        )
        return

    if risk.empty:
        logger.warning(
            "No portfolio risk data found"
        )
        return

    portfolio = positions.merge(
        risk[
            [
                "ticker",
                "risk_score",
                "risk_level"
            ]
        ],
        on="ticker",
        how="left"
    )

    # Risk-adjusted score

    portfolio["adjusted_score"] = (
        portfolio["prediction_score"]
        /
        (1 + portfolio["risk_score"] / 100)
    )

    # Normalize weights

    portfolio["portfolio_weight"] = (
        portfolio["adjusted_score"]
        /
        portfolio["adjusted_score"].sum()
    )

    portfolio = portfolio.sort_values(
        "portfolio_weight",
        ascending=False
    )

    db: Session = SessionLocal()

    try:

        db.query(
            FinalPortfolio
        ).delete()

        db.commit()

        for _, row in portfolio.iterrows():

            position = FinalPortfolio(

                ticker=row["ticker"],

                sector=row["sector"],

                prediction_score=float(
                    row["prediction_score"]
                ),

                risk_score=float(
                    row["risk_score"]
                ),

                portfolio_weight=float(
                    row["portfolio_weight"]
                ),

                created_at=datetime.utcnow()
            )

            db.add(position)

        db.commit()

        logger.info(
            "Final portfolio stored successfully"
        )

    except Exception as e:

        db.rollback()

        logger.error(str(e))

    finally:

        db.close()

    print(
        portfolio[
            [
                "ticker",
                "sector",
                "prediction_score",
                "risk_score",
                "portfolio_weight"
            ]
        ].head(20)
    )


if __name__ == "__main__":

    build_final_portfolio()