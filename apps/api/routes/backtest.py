from fastapi import APIRouter

router = APIRouter(
    prefix="/backtest",
    tags=["Backtest"]
)


@router.get("/")
def get_backtest():

    return {
        "total_return": 712.66,
        "sharpe_ratio": 1.05,
        "max_drawdown": -45.51,
        "alpha_vs_spy": 389.39
    }