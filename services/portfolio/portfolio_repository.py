from shared.configs.database import SessionLocal
from shared.schemas.portfolio_runs import PortfolioRun


def save_portfolio(
    portfolio,
    recommendations,
    committee_review,
    risk_analysis=None,
    portfolio_intelligence=None,
    research_report=None,
    stock_intelligence=None,
    sector_intelligence=None,
) -> int:

    with SessionLocal() as db:
        try:
            run = PortfolioRun(
                portfolio=portfolio,
                recommendations=recommendations,
                committee_review=committee_review,
                risk_analysis=risk_analysis,
                portfolio_intelligence=portfolio_intelligence,
                research_report=research_report,
                stock_intelligence=stock_intelligence,
                sector_intelligence=sector_intelligence,
            )

            db.add(run)
            db.commit()
            db.refresh(run)

            return run.id

        except Exception:
            db.rollback()
            raise


def get_portfolio(
    portfolio_id: int,
) -> PortfolioRun | None:

    with SessionLocal() as db:
        return (
            db.query(PortfolioRun)
            .filter(PortfolioRun.id == portfolio_id)
            .first()
        )


def get_latest_portfolio() -> PortfolioRun | None:

    with SessionLocal() as db:
        return (
            db.query(PortfolioRun)
            .order_by(PortfolioRun.id.desc())
            .first()
        )