import os
import json
from dotenv import load_dotenv
from groq import Groq
from agents.research_agent import ResearchAgent
from services.rag.memory import save_memory
from shared.constants.sector_mapper import SECTOR_MAP
load_dotenv()

class PortfolioManager:

    def __init__(self):

        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.research_agent = ResearchAgent()

    def recommend(self,ticker,question=None):
        if question is None:
            question = (f"Provide an investment analysis for {ticker}"    )
        print("Generating research report...")
        research_report = (self.research_agent.answer(question))

        prompt = f"""
            You are a senior hedge fund portfolio manager.

            You have received the following research report.

            RESEARCH REPORT

            {research_report}

            Based on the report provide:

            1. Investment Rating
            (BUY / HOLD / SELL)

            2. Conviction
            (LOW / MEDIUM / HIGH)

            3. Suggested Position Size
            (1-10 percent)

            4. Investment Horizon

            5. Key Bull Case

            6. Key Bear Case

            7. Final Recommendation

            Return ONLY valid JSON.

            {{
                "ticker": "{ticker}",
                "rating": "BUY",
                "conviction": "HIGH",
                "position_size": 8,
                "horizon": "12-24 months",
                "bull_case": "Explain bullish thesis",
                "bear_case": "Explain bearish thesis",
                "recommendation": "Final recommendation"
            }}
            """

        print("Generating portfolio recommendation...")

        response = (self.client.chat.completions.create(model=self.model,messages=[{"role": "user","content": prompt}]
                    ,temperature=0.2,max_tokens=1000))

        content = (response.choices[0].message.content)
        content = (content.replace("```json", "").replace("```", "").strip())
        save_memory(agent_name="portfolio_manager",memory_key=ticker,memory_value=str(content))
        try:
            return json.loads(content)

        except Exception as e:
            print(f"JSON parsing failed: {e}")
            print(f"Raw response:\n{content}")
            return {"ticker": ticker,"rating": "HOLD","conviction": "LOW","position_size": 1,"horizon": "Unknown",
                "bull_case": "Parsing failed","bear_case": "Parsing failed","recommendation": content}

    def analyze_portfolio(self,portfolio: dict,recommendations: list | None = None,):

    # =====================================
    # Generate AI Recommendations
    # =====================================

        if recommendations is None:

            recommendations = []

            for ticker in portfolio.keys():

                try:
                    recommendation = self.recommend(ticker=ticker)
                    recommendations.append(recommendation)

                except Exception as e:

                    print(f"Recommendation failed for {ticker}: {e}")

        # =====================================
        # Sector Exposure
        # =====================================

        sector_exposure = {}

        for ticker, weight in portfolio.items():

            sector = SECTOR_MAP.get(ticker,"Unknown")

            sector_exposure[sector] = (sector_exposure.get(sector,0)+ weight)

        # =====================================
        # Diversification
        # =====================================

        unique_sectors = len(sector_exposure)
        diversification_score = min(100,unique_sectors * 15)
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

        largest_holding = max(portfolio,key=portfolio.get)

        largest_weight = portfolio[largest_holding]

        if largest_weight > 40:
            risk_score = "High"
        elif largest_weight > 25:
            risk_score = "Medium"
        else:
            risk_score = "Low"

        # =====================================
        # Largest Sector
        # =====================================

        largest_sector = max(sector_exposure,key=sector_exposure.get)

        largest_sector_weight = (sector_exposure[largest_sector])

        # =====================================
        # Health Score
        # =====================================

        health_score = (diversification_score- (largest_weight / 2))
        health_score = max(0,min(100,round(health_score)))

        # =====================================
        # Rebalancing
        # =====================================

        if largest_weight > 25:

            rebalance_action = (f"Reduce exposure to "f"{largest_holding}")

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

        # =====================================
        # Return
        # =====================================

        return {

            "health_score":
                health_score,

            "risk_score":
                risk_score,

            "diversification":
                diversification,

            "diversification_score":
                diversification_score,

            "largest_holding":
                largest_holding,

            "largest_weight":
                round(
                    largest_weight,
                    2
                ),

            "largest_sector":
                largest_sector,

            "largest_sector_weight":
                round(
                    largest_sector_weight,
                    2
                ),

            "sector_exposure":
                sector_exposure,

            "manager_commentary":
                manager_commentary,

            "rebalance_action":
                rebalance_action,

            "recommendations":
                recommendations
        }
    def analyze_risk(self,portfolio: dict):
    
        largest_holding = max(
            portfolio,
            key=portfolio.get
        )

        largest_weight = portfolio[
            largest_holding
        ]

        # concentration risk

        if largest_weight >= 40:
            concentration_risk = "HIGH"

        elif largest_weight >= 25:
            concentration_risk = "MEDIUM"

        else:
            concentration_risk = "LOW"

        # portfolio risk score

        risk_score = round(
            largest_weight * 0.2,
            1
        )

        return {

            "largest_holding":
                largest_holding,

            "largest_weight":
                largest_weight,

            "concentration_risk":
                concentration_risk,

            "risk_score":
                risk_score
        }
if __name__ == "__main__":

    manager = PortfolioManager()
    result = manager.recommend(ticker="TSLA",question="What did Tesla management say about AI?")

    print("\n")
    print("=" * 80)
    print("PORTFOLIO RECOMMENDATION")
    print("=" * 80)
    print("\n")
    print(json.dumps(result,indent=4))