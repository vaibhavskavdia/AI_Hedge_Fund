import json
from agents.portfolio_manager import PortfolioManager
from agents.investment_committee import InvestmentCommittee
from services.rag.memory import save_memory

class PortfolioConstructionAgent:

    def __init__(self):

        self.portfolio_manager = PortfolioManager()
        self.committee = InvestmentCommittee()
        
    def build_portfolio(self, tickers):

        recommendations = []

        for ticker in tickers:

            print(f"Analyzing {ticker}...")

            result = self.portfolio_manager.recommend(ticker=ticker)

            recommendations.append(result)

        scores = []

        for rec in recommendations:

            conviction = rec["conviction"]

            if conviction == "HIGH":
                score = 3

            elif conviction == "MEDIUM":
                score = 2

            else:
                score = 1

            scores.append(score)

        total_score = sum(scores)

        portfolio = {}

        for rec, score in zip(recommendations,scores):

            weight = round((score / total_score) * 100,2)
            portfolio[rec["ticker"]] = weight

        committee_review = self.committee.review(portfolio)

        result = {"portfolio": portfolio,"recommendations": recommendations,"committee_review": committee_review}

        save_memory(agent_name="portfolio_constructor",memory_key=",".join(tickers),memory_value=json.dumps(result))

        return result


if __name__ == "__main__":

    agent = PortfolioConstructionAgent()

    result = agent.build_portfolio(["TSLA","NVDA","AAPL"])

    print(json.dumps(result,indent=4))