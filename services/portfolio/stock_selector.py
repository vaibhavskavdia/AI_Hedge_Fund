from services.portfolio.portfolio_ranker import PortfolioRanker
from services.portfolio.universe_builder import UniverseBuilder


class StockSelector:
    """
    Selects stocks for portfolio construction.

    Responsibilities:
        1. Build investable universe
        2. Apply sector filters
        3. Rank stocks
        4. Return top N tickers

    This class does NOT perform AI analysis.
    """

    def __init__(self):

        self.universe_builder = UniverseBuilder()
        self.ranker = PortfolioRanker()

    def select(
        self,
        risk_profile: str,
        preferred_sectors: list[str],
        max_holdings: int,
    ) -> list[str]:

        # -----------------------------------------
        # Build Universe
        # -----------------------------------------

        universe = self.universe_builder.build()

        if universe.empty:
            return []

        # -----------------------------------------
        # Sector Filtering
        # -----------------------------------------

        if preferred_sectors:

            universe = universe[
                universe["sector"].isin(preferred_sectors)
            ]

        if universe.empty:
            return []

        # -----------------------------------------
        # Rank Universe
        # -----------------------------------------

        ranked = self.ranker.rank(
            universe=universe,
            risk_profile=risk_profile,
        )

        # -----------------------------------------
        # Select Top Holdings
        # -----------------------------------------

        ranked = ranked.head(max_holdings)

        return ranked["ticker"].tolist()


if __name__ == "__main__":

    selector = StockSelector()

    tickers = selector.select(
        risk_profile="Balanced",
        preferred_sectors=[
            "Technology",
            "Healthcare",
        ],
        max_holdings=10,
    )

    print("\nSelected Tickers:\n")
    print(tickers)