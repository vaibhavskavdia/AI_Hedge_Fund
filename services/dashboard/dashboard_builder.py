from agents.portfolio_construction_agent import PortfolioConstructionAgent
from agents.portfolio_manager import PortfolioManager
from services.portfolio.portfolio_repository import save_portfolio
from services.risk.risk_engine import RiskEngine
from services.jobs.job_manager import update_job

class DashboardBuilder:

    def __init__(self):

        self.constructor = PortfolioConstructionAgent()
        self.manager = PortfolioManager()
        self.risk = RiskEngine()

    def build_dashboard(self, tickers,job_id):

        # ---------------------------------
        # Step 1 : Build Portfolio
        # ---------------------------------
        update_job(
            job_id,
            progress=5,
            step="Building Portfolio"
        )

        portfolio_result = self.constructor.build_portfolio(
            tickers
        )
        update_job(
            job_id,
            progress=40,
            step="Generating Portfolio Intelligence"
        )
        portfolio = portfolio_result["portfolio"]

        recommendations = portfolio_result["recommendations"]

        committee_review = portfolio_result["committee_review"]

        # ---------------------------------
        # Step 2 : Portfolio Intelligence
        # ---------------------------------

        intelligence = self.manager.analyze_portfolio(
            portfolio=portfolio,
            recommendations=recommendations,
        )
        update_job(
            job_id,
            progress=70,
            step="Generating Risk Analysis"
        )
        # ---------------------------------
        # Step 3 : Risk
        # ---------------------------------

        risk = self.manager.analyze_risk(
            portfolio
        )
        update_job(
            job_id,
            progress=90,
            step="Saving Portfolio"
        )
        # ---------------------------------
        # Step 4 : Save Everything
        # ---------------------------------

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
        update_job(
            job_id,
            progress=100,
            status="completed",
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