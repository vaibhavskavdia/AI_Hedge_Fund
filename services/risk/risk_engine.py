import pandas as pd

from sqlalchemy import text
from sqlalchemy.orm import Session

from shared.configs.database import engine
from shared.configs.database import SessionLocal

from shared.schemas.features import FeatureStore
from shared.schemas.portfolio_risk import PortfolioRisk

from logger import logger


PORTFOLIO_QUERY = """
SELECT *
FROM portfolio_positions;
"""


class RiskEngine:

    def get_latest_features(self, ticker):

        db = SessionLocal()

        row = (
            db.query(FeatureStore)
            .filter(
                FeatureStore.ticker == ticker
            )
            .order_by(
                FeatureStore.timestamp.desc()
            )
            .first()
        )

        db.close()

        return row

    def calculate_risk_score(self, row):

        score = 0

        if hasattr(row, "volatility_10"):

            score += row.volatility_10 * 100

        if hasattr(row, "volume_change"):

            score += abs(
                row.volume_change
            ) * 10

        if hasattr(row, "volume_spike"):

            if row.volume_spike > 2:

                score += 5

            elif row.volume_spike > 1.5:

                score += 3

        if hasattr(row, "rsi_14"):

            if row.rsi_14 > 70:

                score += 5

            elif row.rsi_14 < 30:

                score += 5

        if hasattr(row, "relative_strength"):

            if row.relative_strength < -0.03:

                score += 5

            elif row.relative_strength < -0.01:

                score += 3

            elif row.relative_strength > 0.03:

                score -= 3

        if hasattr(row, "dist_52w_high"):

            if row.dist_52w_high < 0.80:

                score += 4

            elif row.dist_52w_high < 0.90:

                score += 2

        if hasattr(row, "avg_sentiment_score"):

            if row.avg_sentiment_score < -0.5:

                score += 5

            elif row.avg_sentiment_score < -0.2:

                score += 3

            elif row.avg_sentiment_score > 0.5:

                score -= 2

        return round(
            max(score, 0),
            2
        )

    def classify_risk(self, score):

        if score < 5:

            return "LOW"

        elif score < 15:

            return "MEDIUM"

        return "HIGH"

    def get_position_size(self, risk_level):

        if risk_level == "LOW":

            return 10

        elif risk_level == "MEDIUM":

            return 7

        return 5

    def get_stop_loss(self, risk_level):

        if risk_level == "LOW":

            return 15

        elif risk_level == "MEDIUM":

            return 12

        return 8

    def evaluate_position(self, row):

        risk_score = self.calculate_risk_score(
            row
        )

        risk_level = self.classify_risk(
            risk_score
        )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "max_position_size":
                self.get_position_size(
                    risk_level
                ),
            "stop_loss_percent":
                self.get_stop_loss(
                    risk_level
                )
        }
        
    def risk_recommendation(self,risk_score):

        if risk_score > 20:
            return "Reduce Position"

        elif risk_score > 10:
            return "Monitor Closely"

        return "Healthy Position"   
     

    def run(self):

        logger.info(
            "Loading portfolio"
        )

        portfolio = pd.read_sql(
            text(PORTFOLIO_QUERY),
            engine
        )

        db: Session = SessionLocal()

        try:

            db.query(
                PortfolioRisk
            ).delete()

            db.commit()

            for _, stock in portfolio.iterrows():

                features = (
                    self.get_latest_features(
                        stock["ticker"]
                    )
                )

                if features is None:

                    continue

                result = (
                    self.evaluate_position(
                        features
                    )
                )

                risk_row = PortfolioRisk(

                    ticker=stock["ticker"],

                    risk_score=
                        result["risk_score"],

                    risk_level=
                        result["risk_level"],

                    max_position_size=
                        result[
                            "max_position_size"
                        ],

                    stop_loss_percent=
                        result[
                            "stop_loss_percent"
                        ]
                )

                db.add(risk_row)

            db.commit()

            logger.info(
                "Risk analysis completed"
            )

        except Exception as e:

            db.rollback()

            logger.error(str(e))

        finally:

            db.close()


if __name__ == "__main__":

    risk_engine = RiskEngine()

    risk_engine.run()