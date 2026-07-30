from threading import Thread

from services.dashboard.dashboard_builder import DashboardBuilder
from services.jobs.job_manager import create_job
from services.portfolio.stock_selector import StockSelector
from apps.api.schemas.requests.portfolio_request import PortfolioRequest


class PortfolioService:

    def __init__(self):

        self.dashboard_builder = DashboardBuilder()
        self.stock_selector = StockSelector()

    def generate(
        self,
        request: PortfolioRequest,
    ) -> dict:
        """
        Generates a portfolio from user preferences.

        Flow:
            User Preferences
                    ↓
            Stock Selector
                    ↓
            Dashboard Builder
                    ↓
            Background Job
        """

        tickers = self.stock_selector.select(
            risk_profile=request.risk_profile,
            preferred_sectors=request.preferred_sectors,
            max_holdings=request.max_holdings,
        )

        if not tickers:
            return {
                "job_id": None,
                "status": "failed",
                "result": None,
                "error": "No stocks matched the selected preferences.",
            }

        job_id = create_job()

        Thread(
            target=self.dashboard_builder.build_dashboard,
            args=(tickers, job_id),
            daemon=True,
        ).start()

        return {
            "job_id": job_id,
            "status": "queued",
            "selected_tickers": tickers,
            "result": None,
            "error": None,
        }