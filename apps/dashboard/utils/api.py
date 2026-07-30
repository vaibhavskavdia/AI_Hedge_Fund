import requests
from typing import Any


BASE_URL = "http://127.0.0.1:8000"


class APIClient:

    def __init__(self):
        self.base_url = BASE_URL

    def _get(self, endpoint: str) -> Any:

        response = requests.get(
            f"{self.base_url}{endpoint}",
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def _post(
        self,
        endpoint: str,
        payload: dict | None = None,
    ) -> Any:

        response = requests.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        return response.json()

    # ======================================================
    # AI Portfolio
    # ======================================================

    def generate_portfolio(
        self,
        investment_amount: float,
        risk_profile: str,
        preferred_sectors: list[str],
        max_holdings: int,
    ):

        payload = {
            "investment_amount": investment_amount,
            "risk_profile": risk_profile,
            "preferred_sectors": preferred_sectors,
            "max_holdings": max_holdings,
        }

        return self._post(
            "/portfolio/ai-portfolio",
            payload,
        )

    def latest_portfolio(self):

        return self._get(
            "/portfolio/latest"
        )

    def portfolio_positions(self):

        return self._get(
            "/portfolio/"
        )

    def portfolio_intelligence(self):

        return self._get(
            "/portfolio/portfolio-intelligence"
        )

    def portfolio_job(
        self,
        job_id: str,
    ):

        return self._get(
            f"/portfolio/job/{job_id}"
        )

    # ======================================================
    # Recommendations
    # ======================================================

    def recommend_portfolio(
        self,
        investment_amount: float,
        top_n: int,
        risk_profile: str,
    ):

        return self._get(
            f"/portfolio/recommend"
            f"?investment_amount={investment_amount}"
            f"&top_n={top_n}"
            f"&risk_profile={risk_profile}"
        )

    def ai_recommendation(
        self,
        ticker: str,
    ):

        return self._post(
            "/portfolio/ai-recommendation",
            {
                "ticker": ticker,
            },
        )

    # ======================================================
    # Risk
    # ======================================================

    def latest_risk(self):

        return self._get(
            "/risk/latest"
        )

    # ======================================================
    # Research
    # ======================================================

    def research(
        self,
        ticker: str,
    ):

        return self._get(
            f"/research/{ticker}"
        )

    # ======================================================
    # Stock Intelligence
    # ======================================================

    def stock(
        self,
        ticker: str,
    ):

        return self._get(
            f"/stock/{ticker}"
        )


api = APIClient()