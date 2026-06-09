from fastapi import FastAPI

from apps.api.routes.predictions import router as predictions_router
from apps.api.routes.portfolio import router as portfolio_router
from apps.api.routes.backtest import router as backtest_router

app = FastAPI(
    title="AI Hedge Fund API",
    version="1.0"
)

app.include_router(predictions_router)
app.include_router(portfolio_router)
app.include_router(backtest_router)


@app.get("/")
def home():
    return {"message": "AI Hedge Fund API Running"}