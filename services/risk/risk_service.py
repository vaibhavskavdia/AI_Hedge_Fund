class RiskService:
    """
    Computes portfolio-level risk metrics.
    """

    def analyze(self, portfolio: dict) -> dict:
        """
        Analyze portfolio concentration risk.

        Args:
            portfolio: Dictionary of ticker -> portfolio weight.

        Returns:
            Dictionary containing risk metrics.
        """

        if not portfolio:
            return {
                "largest_holding": None,
                "largest_weight": 0,
                "concentration_risk": "UNKNOWN",
                "risk_score": 0,
            }

        largest_holding = max(
            portfolio,
            key=portfolio.get,
        )

        largest_weight = portfolio[largest_holding]

        # Concentration Risk
        if largest_weight >= 40:
            concentration_risk = "HIGH"

        elif largest_weight >= 25:
            concentration_risk = "MEDIUM"

        else:
            concentration_risk = "LOW"

        # Portfolio Risk Score
        risk_score = round(largest_weight * 0.2, 1)

        return {
            "largest_holding": largest_holding,
            "largest_weight": largest_weight,
            "concentration_risk": concentration_risk,
            "risk_score": risk_score,
        }