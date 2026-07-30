from sqlalchemy.orm import Session

from shared.schemas.features import FeatureStore
from shared.schemas.portfolio_positions import PortfolioPosition
from shared.schemas.apis.portfolio import PortfolioRecommendation
from services.risk.risk_engine import RiskEngine


class RecommendationService:

    def __init__(self):
        self.risk_engine = RiskEngine()

    def recommend(
        self,
        db: Session,
        investment_amount: float,
        top_n: int,
        risk_profile: str,
    ) -> list[PortfolioRecommendation]:

        latest_timestamp = (
            db.query(PortfolioPosition.timestamp)
            .order_by(PortfolioPosition.timestamp.desc())
            .first()
        )

        if not latest_timestamp:
            return []

        positions = (
            db.query(PortfolioPosition)
            .filter(
                PortfolioPosition.timestamp == latest_timestamp[0]
            )
            .all()
        )

        portfolio_data = []

        for position in positions:

            feature = (
                db.query(FeatureStore)
                .filter(FeatureStore.ticker == position.ticker)
                .order_by(FeatureStore.timestamp.desc())
                .first()
            )

            if not feature:
                continue

            risk_score = self.risk_engine.evaluate_position(
                feature
            )["risk_score"]

            portfolio_data.append(
                {
                    "position": position,
                    "risk_score": risk_score,
                }
            )

        portfolio_data = self._sort(
            portfolio_data,
            risk_profile,
        )[:top_n]

        return self._build_response(
            portfolio_data,
            investment_amount,
        )

    def _sort(
        self,
        portfolio_data,
        risk_profile,
    ):

        profile = risk_profile.lower()

        if profile == "conservative":
            return sorted(
                portfolio_data,
                key=lambda x: x["risk_score"],
            )

        if profile == "aggressive":
            return sorted(
                portfolio_data,
                key=lambda x:
                (
                    x["position"].prediction_probability
                    - x["risk_score"] * 0.001
                ),
                reverse=True,
            )

        return sorted(
            portfolio_data,
            key=lambda x:
            (
                x["position"].prediction_probability
                - x["risk_score"] * 0.005
            ),
            reverse=True,
        )

    def _build_response(
        self,
        portfolio_data,
        investment_amount,
    ):

        positions = [
            item["position"]
            for item in portfolio_data
        ]

        if not positions:
            return []

        total_weight = sum(
            p.weight
            for p in positions
        )

        recommendations = []

        for position in positions:

            normalized_weight = (
                position.weight / total_weight
            )

            recommendations.append(
                PortfolioRecommendation(
                    ticker=position.ticker,
                    weight=round(normalized_weight, 4),
                    allocation=round(
                        normalized_weight * investment_amount,
                        2,
                    ),
                    prediction_probability=round(
                        position.prediction_probability,
                        4,
                    ),
                )
            )

        return recommendations