from shared.constants.sector_mapper import SECTOR_MAP


class PortfolioIntelligenceService:
    """
    Computes portfolio intelligence and health metrics.
    """

    def analyze(
        self,
        portfolio: dict,
        recommendations: list | None = None,
    ) -> dict:
        """
        Analyze a portfolio and generate portfolio-level intelligence.

        Args:
            portfolio: Dictionary of ticker -> weight.
            recommendations: Existing AI recommendations (optional).

        Returns:
            Dictionary containing portfolio intelligence metrics.
        """

        if not portfolio:
            return {
                "health_score": 0,
                "risk_score": "Unknown",
                "diversification": "Unknown",
                "diversification_score": 0,
                "largest_holding": None,
                "largest_weight": 0,
                "largest_sector": None,
                "largest_sector_weight": 0,
                "sector_exposure": {},
                "manager_commentary": "No portfolio available.",
                "rebalance_action": "No action.",
                "recommendations": recommendations or [],
            }

        if recommendations is None:
            recommendations = []

        # =====================================
        # Sector Exposure
        # =====================================

        sector_exposure = {}

        for ticker, weight in portfolio.items():

            sector = SECTOR_MAP.get(ticker, "Unknown")

            sector_exposure[sector] = (
                sector_exposure.get(sector, 0) + weight
            )

        # =====================================
        # Diversification
        # =====================================

        unique_sectors = len(sector_exposure)

        diversification_score = min(
            100,
            unique_sectors * 15,
        )

        if diversification_score >= 80:
            diversification = "Excellent"

        elif diversification_score >= 60:
            diversification = "Good"

        elif diversification_score >= 40:
            diversification = "Moderate"

        else:
            diversification = "Low"

        # =====================================
        # Concentration Risk
        # =====================================

        largest_holding = max(
            portfolio,
            key=portfolio.get,
        )

        largest_weight = portfolio[
            largest_holding
        ]

        if largest_weight > 40:
            risk_score = "High"

        elif largest_weight > 25:
            risk_score = "Medium"

        else:
            risk_score = "Low"

        # =====================================
        # Largest Sector
        # =====================================

        largest_sector = max(
            sector_exposure,
            key=sector_exposure.get,
        )

        largest_sector_weight = sector_exposure[
            largest_sector
        ]

        # =====================================
        # Health Score
        # =====================================

        health_score = (
            diversification_score
            - (largest_weight / 2)
        )

        health_score = max(
            0,
            min(
                100,
                round(health_score),
            ),
        )

        # =====================================
        # Rebalancing
        # =====================================

        if largest_weight > 25:

            rebalance_action = (
                f"Reduce exposure to {largest_holding}"
            )

        else:

            rebalance_action = (
                "Portfolio balanced"
            )

        # =====================================
        # Manager Commentary
        # =====================================

        manager_commentary = f"""
Portfolio is primarily concentrated in {largest_sector}.

Largest position is {largest_holding}
with {largest_weight:.2f}% allocation.

Largest sector exposure is {largest_sector}
at {largest_sector_weight:.2f}%.

Diversification level is {diversification}.

Current concentration risk is {risk_score}.

Recommendation:
{rebalance_action}.
"""

        return {
            "health_score": health_score,
            "risk_score": risk_score,
            "diversification": diversification,
            "diversification_score": diversification_score,
            "largest_holding": largest_holding,
            "largest_weight": round(largest_weight, 2),
            "largest_sector": largest_sector,
            "largest_sector_weight": round(
                largest_sector_weight,
                2,
            ),
            "sector_exposure": sector_exposure,
            "manager_commentary": manager_commentary,
            "rebalance_action": rebalance_action,
            "recommendations": recommendations,
        }