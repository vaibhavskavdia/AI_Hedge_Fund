import os
import requests

from datetime import datetime
from dotenv import load_dotenv

from shared.configs.database import SessionLocal
from shared.schemas.raw_documents import RawDocument

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
    "JPM",
    "SPY"
]
def get_transcript(ticker):

    url = (
        "https://www.alphavantage.co/query"
        f"?function=EARNINGS_CALL_TRANSCRIPT"
        f"&symbol={ticker}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url, timeout=30)

    print(response.status_code)
    print(response.text[:500])

    return response.json()

print(get_transcript("AAPL"))