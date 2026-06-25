from shared.schemas.portfolio_runs import PortfolioRun
from shared.configs.database import SessionLocal


def save_portfolio(
    portfolio,
    recommendations,
    committee_review
):

    db = SessionLocal()

    run = PortfolioRun(
        portfolio=portfolio,
        recommendations=recommendations,
        committee_review=committee_review
    )

    db.add(run)
    db.commit()
    db.refresh(run)

    portfolio_id = run.id

    db.close()

    return portfolio_id

def get_portfolio(portfolio_id):

    db = SessionLocal()

    run = (
        db.query(PortfolioRun)
        .filter(
            PortfolioRun.id == portfolio_id
        )
        .first()
    )

    db.close()

    return run

def get_latest_portfolio():
    db = SessionLocal()

    portfolio = (
        db.query(PortfolioRun)
        .order_by(PortfolioRun.id.desc())
        .first()
    )

    db.close()

    return portfolio