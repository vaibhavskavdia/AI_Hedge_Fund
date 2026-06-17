import os
import json
from dotenv import load_dotenv
from groq import Groq
from services.rag.memory import save_memory
load_dotenv()

class InvestmentCommittee:
    def __init__(self):

        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"

    def review(self, portfolio):

        prompt = f"""
                    You are an institutional investment committee.

                    Review the following portfolio:

                    {json.dumps(portfolio, indent=4)}

                    Provide:

                    1. Portfolio Rating
                    2. Top Pick
                    3. Biggest Risk
                    4. Diversification Assessment
                    5. Final Approval

                    Return ONLY valid JSON.

                    {{
                        "portfolio_rating":"",
                        "top_pick":"",
                        "biggest_risk":"",
                        "diversification":"",
                        "approved":true,
                        "committee_summary":""
                    }}
                    """

        response = self.client.chat.completions.create(model=self.model,messages=[{"role": "user","content": prompt}],temperature=0.2)
        content = response.choices[0].message.content
        content = (content.replace("```json", "").replace("```", "").strip())
        save_memory(agent_name="investment_committee",memory_key="committee_review",memory_value=str(response))
        return json.loads(content)


if __name__ == "__main__":

    sample_portfolio = {
        "TSLA": 25,
        "NVDA": 40,
        "AAPL": 35}

    committee = InvestmentCommittee()

    result = committee.review(sample_portfolio)

    print(json.dumps(result,indent=4))