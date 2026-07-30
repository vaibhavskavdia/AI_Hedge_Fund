from agents.portfolio_construction_agent import PortfolioConstructionAgent

from services.jobs.job_manager import update_job
from services.portfolio.portfolio_repository import save_portfolio
from services.portfolio.intelligence_service import PortfolioIntelligenceService
from services.risk.risk_service import RiskService


class DashboardBuilder:

    def __init__(self):

        self.constructor = PortfolioConstructionAgent()
        self.intelligence_service = PortfolioIntelligenceService()
        self.risk_service = RiskService()

    def build_dashboard(self, tickers, job_id):

        try:

            # ---------------------------------
            # Step 1 : Build Portfolio
            # ---------------------------------

            update_job(
                job_id,
                status="running",
                progress=5,
                step="Building Portfolio",
            )

            portfolio_result = self.constructor.build_portfolio(
                tickers
            )

            portfolio = portfolio_result["portfolio"]
            recommendations = portfolio_result["recommendations"]
            committee_review = portfolio_result["committee_review"]

            # ---------------------------------
            # Step 2 : Portfolio Intelligence
            # ---------------------------------

            update_job(
                job_id,
                progress=40,
                step="Generating Portfolio Intelligence",
            )

            intelligence = self.intelligence_service.analyze(
                portfolio=portfolio,
                recommendations=recommendations,
            )

            # ---------------------------------
            # Step 3 : Risk Analysis
            # ---------------------------------

            update_job(
                job_id,
                progress=70,
                step="Generating Risk Analysis",
            )

            risk = self.risk_service.analyze(
                portfolio
            )

            # ---------------------------------
            # Step 4 : Save Portfolio
            # ---------------------------------

            update_job(
                job_id,
                progress=90,
                step="Saving Portfolio",
            )

            portfolio_id = save_portfolio(
                portfolio=portfolio,
                recommendations=recommendations,
                committee_review=committee_review,
                risk_analysis=risk,
                portfolio_intelligence=intelligence,
                research_report=None,
                stock_intelligence=None,
                sector_intelligence=None,
            )

            # ---------------------------------
            # Step 5 : Complete
            # ---------------------------------

            update_job(
                job_id,
                status="completed",
                progress=100,
                step="Completed",
                portfolio_id=portfolio_id,
            )

            return {
                "portfolio_id": portfolio_id,
                "portfolio": portfolio,
                "recommendations": recommendations,
                "committee_review": committee_review,
                "portfolio_intelligence": intelligence,
                "risk": risk,
            }

        except Exception as e:

            print(f"\nDashboard Builder Failed:\n{e}\n")

            update_job(
                job_id,
                status="failed",
                step="Failed",
                error=str(e),
            )

            raise