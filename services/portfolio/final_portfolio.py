import pandas as pd

from sqlalchemy import text
from sqlalchemy.orm import Session

from shared.configs.database import engine
from shared.configs.database import SessionLocal

from shared.schemas.final_portfolio import FinalPortfolio


PREDICTIONS_QUERY = """
SELECT *
FROM portfolio_positions
"""

RISK_QUERY = """
SELECT *
FROM portfolio_risk
"""

FEATURE_QUERY = """
SELECT *
FROM feature_store
"""


def get_recommendation(score):

    if score >= 80:
        return "STRONG BUY"

    if score >= 65:
        return "BUY"

    if score >= 50:
        return "HOLD"

    return "AVOID"


def build_final_portfolio():

    portfolio = pd.read_sql(
        text(PREDICTIONS_QUERY),
        engine
    )

    risk = pd.read_sql(
        text(RISK_QUERY),
        engine
    )

    features = pd.read_sql(
        text(FEATURE_QUERY),
        engine
    )

    features = (
        features
        .sort_values("timestamp")
        .drop_duplicates(
            subset=["ticker"],
            keep="last"
        )
    )

    final_df = portfolio.merge(
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

    final_df = final_df.merge(
        features[
            [
                "ticker",
                "future_return_5d"
            ]
        ],
        on="ticker",
        how="left"
    )

    final_df["expected_return_5d"] = (
        final_df["future_return_5d"] * 100
    )

    final_df["win_rate"] = (
        final_df["prediction_score"] * 100
    )

    final_df["portfolio_score"] = (
        (
            final_df["prediction_score"] * 100
        )
        +
        (
            final_df["expected_return_5d"] * 2
        )
        -
        (
            final_df["risk_score"]
        )
    )

    final_df["recommendation"] = (
        final_df["portfolio_score"]
        .apply(get_recommendation)
    )

    final_df = final_df.sort_values(
        "portfolio_score",
        ascending=False
    )

    db: Session = SessionLocal()

    try:

        db.query(FinalPortfolio).delete()

        db.commit()

        for _, row in final_df.iterrows():

            record = FinalPortfolio(

                ticker=row["ticker"],

                sector=row.get(
                    "sector",
                    "Unknown"
                ),

                prediction_score=float(
                    row["prediction_score"]
                ),

                expected_return_5d=float(
                    row["expected_return_5d"]
                ),

                risk_score=float(
                    row["risk_score"]
                ),

                risk_level=str(
                    row["risk_level"]
                ),

                win_rate=float(
                    row["win_rate"]
                ),

                portfolio_score=float(
                    row["portfolio_score"]
                ),

                weight=float(
                    row["weight"]
                ),

                recommendation=str(
                    row["recommendation"]
                )
            )

            db.add(record)

        db.commit()

        print(
            "Final portfolio generated successfully!"
        )

    except Exception as e:

        db.rollback()

        print(e)

    finally:

        db.close()


if __name__ == "__main__":

    build_final_portfolio()