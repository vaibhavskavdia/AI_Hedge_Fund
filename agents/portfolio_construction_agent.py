import json

from agents.investment_committee import InvestmentCommittee
from agents.portfolio_manager import PortfolioManager

from services.portfolio.portfolio_allocator import PortfolioAllocator
from services.rag.memory import save_memory


class PortfolioConstructionAgent:

    def __init__(self):

        self.portfolio_manager = PortfolioManager()
        self.committee = InvestmentCommittee()
        self.allocator = PortfolioAllocator()

    def build_portfolio(self, tickers):

        recommendations = []

        for ticker in tickers:

            print(f"Analyzing {ticker}...")

            try:

                recommendation = self.portfolio_manager.recommend(
                    ticker=ticker
                )

                recommendations.append(recommendation)

            except Exception as e:

                print(f"{ticker} failed: {e}")

                recommendations.append(
                    {
                        "ticker": ticker,
                        "rating": "HOLD",
                        "conviction": "LOW",
                        "position_size": 1,
                        "horizon": "Unknown",
                        "bull_case": "Recommendation generation failed.",
                        "bear_case": "Recommendation generation failed.",
                        "recommendation": "Skipped due to error.",
                    }
                )

        # ---------------------------------
        # Allocate Portfolio
        # ---------------------------------

        portfolio = self.allocator.allocate(
            recommendations
        )

        # ---------------------------------
        # Investment Committee Review
        # ---------------------------------

        committee_review = self.committee.review(
            portfolio
        )

        result = {
            "portfolio": portfolio,
            "recommendations": recommendations,
            "committee_review": committee_review,
        }

        save_memory(
            agent_name="portfolio_constructor",
            memory_key=",".join(tickers),
            memory_value=json.dumps(result),
        )

        return result


if __name__ == "__main__":

    agent = PortfolioConstructionAgent()

    result = agent.build_portfolio(
        ["TSLA", "NVDA", "AAPL"]
    )

    print(json.dumps(result, indent=4))