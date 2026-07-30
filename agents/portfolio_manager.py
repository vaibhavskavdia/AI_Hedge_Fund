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
        try:
            response = (self.client.chat.completions.create(model=self.model,messages=[{"role": "user","content": prompt}]
                    ,temperature=0.2,max_tokens=1000))
        except Exception as e:
            print(f"Error occurred while calling Groq API for {ticker}: {e}")
            return {"ticker": ticker,"rating": "HOLD","conviction": "LOW","position_size": 1,"horizon": "Unknown",
                "bull_case": "API call failed","bear_case": "API call failed","recommendation": "Skipped due to API error."}
        print(">>> Groq API returned")
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

    

if __name__ == "__main__":

    manager = PortfolioManager()
    result = manager.recommend(ticker="TSLA",question="What did Tesla management say about AI?")

    print("\n")
    print("=" * 80)
    print("PORTFOLIO RECOMMENDATION")
    print("=" * 80)
    print("\n")
    print(json.dumps(result,indent=4))