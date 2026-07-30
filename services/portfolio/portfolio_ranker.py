import pandas as pd


class PortfolioRanker:
    """
    Centralized ranking engine for portfolio construction.

    Every service that needs ranked stocks should use this class.

    Current Score:
        portfolio_score =
            70% Prediction Probability
          + 30% Risk Adjustment

    Future versions can easily incorporate:
        - Expected Return
        - Sharpe Ratio
        - Volatility
        - Earnings Growth
        - Sentiment
        - AI Conviction
    """

    def rank(
        self,
        universe: pd.DataFrame,
        risk_profile: str,
    ) -> pd.DataFrame:
        """
        Rank the investable universe.

        Parameters
        ----------
        universe : pd.DataFrame
            Expected columns:
                ticker
                sector
                prediction_probability

            Optional columns:
                risk_score

        risk_profile : str
            Conservative | Balanced | Aggressive

        Returns
        -------
        pd.DataFrame
            Ranked dataframe with an additional
            portfolio_score column.
        """

        if universe.empty:
            return universe

        df = universe.copy()

        # --------------------------------------------------
        # Prediction Score
        # --------------------------------------------------

        df["prediction_score"] = (
            df["prediction_probability"]
        )

        # --------------------------------------------------
        # Risk Score
        # --------------------------------------------------

        if "risk_score" not in df.columns:

            df["risk_score"] = 50.0

        max_risk = df["risk_score"].max()

        if max_risk == 0:
            max_risk = 1

        df["normalized_risk"] = (
            df["risk_score"] / max_risk
        )

        # --------------------------------------------------
        # Portfolio Score
        # --------------------------------------------------

        profile = risk_profile.lower()

        if profile == "conservative":

            prediction_weight = 0.40
            risk_weight = 0.60

        elif profile == "balanced":

            prediction_weight = 0.70
            risk_weight = 0.30

        elif profile == "aggressive":

            prediction_weight = 0.90
            risk_weight = 0.10

        else:

            prediction_weight = 0.70
            risk_weight = 0.30

        df["portfolio_score"] = (
            prediction_weight * df["prediction_score"]
            +
            risk_weight * (1 - df["normalized_risk"])
        )

        df = df.sort_values(
            by="portfolio_score",
            ascending=False,
        ).reset_index(drop=True)

        return df