class PortfolioAllocator:
    """
    Converts AI recommendations into portfolio weights.

    Allocation Strategy
    -------------------
    Score =
        position_size × conviction_multiplier

    The scores are normalized to produce portfolio weights
    that sum to 100%.
    """

    CONVICTION_MULTIPLIERS = {
        "HIGH": 1.25,
        "MEDIUM": 1.00,
        "LOW": 0.75,
    }

    def allocate(
        self,
        recommendations: list[dict],
    ) -> dict:
        """
        Allocate portfolio weights.

        Args:
            recommendations:
                List of AI recommendation dictionaries.

        Returns:
            Dictionary[ticker, weight_percentage]
        """

        if not recommendations:
            return {}

        scored_positions = []

        for recommendation in recommendations:

            rating = recommendation.get(
                "rating",
                "BUY",
            ).upper()

            # Ignore SELL recommendations
            if rating == "SELL":
                continue

            conviction = recommendation.get(
                "conviction",
                "MEDIUM",
            ).upper()

            multiplier = self.CONVICTION_MULTIPLIERS.get(
                conviction,
                1.0,
            )

            position_size = recommendation.get(
                "position_size",
                5,
            )

            try:
                position_size = float(position_size)
            except (TypeError, ValueError):
                position_size = 5.0

            score = position_size * multiplier

            scored_positions.append(
                (
                    recommendation["ticker"],
                    score,
                )
            )

        if not scored_positions:
            return {}

        total_score = sum(
            score
            for _, score in scored_positions
        )

        if total_score <= 0:
            return {}

        portfolio = {}

        for ticker, score in scored_positions:

            portfolio[ticker] = round(
                (score / total_score) * 100,
                2,
            )

        return portfolio