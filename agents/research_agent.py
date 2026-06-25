import os
from dotenv import load_dotenv
from groq import Groq
from services.rag.retrieve import retrieve_context
load_dotenv()
class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
    def answer(self, query):
        contexts = retrieve_context(query)
        context_text = "\n\n".join([  f"""
                Ticker: {chunk['ticker']}

                {chunk['content']}"""
        for chunk in contexts])
        prompt = f"""
You are a senior hedge fund research analyst.
Use ONLY the provided context.
Context:
{context_text}
Question:
{query}
Provide:
1. Key Findings
2. Risks
3. Opportunities
4. Investment Takeaway
Answer in professional analyst style.
"""
        response = self.client.chat.completions.create(model=self.model,messages=[{
                    "role": "user",
                    "content": prompt}],temperature=0.2,max_tokens=2000)
        return response.choices[0].message.content    
if __name__ == "__main__":
    agent = ResearchAgent()
    response = agent.answer("What did Tesla management say about AI?")
    print(response)