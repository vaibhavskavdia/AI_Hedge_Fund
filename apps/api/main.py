from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routes.predictions import router as predictions_router
from apps.api.routes.portfolio import router as portfolio_router
from apps.api.routes.research import router as research_router
from apps.api.routes.risk import router as risk_router
from apps.api.routes.portfolio_intelligence import (
    router as intelligence_router,
)
from apps.api.routes.stock_intelligence import (
    router as stock_intelligence_router,
)
from apps.api.routes.sector_intelligence import (
    router as sector_intelligence_router,
)

app = FastAPI(
    title="AI Hedge Fund API",
    version="1.0",
)

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Routes
# ----------------------------
app.include_router(predictions_router)
app.include_router(portfolio_router)
app.include_router(research_router)
app.include_router(intelligence_router)
app.include_router(stock_intelligence_router)
app.include_router(sector_intelligence_router)

app.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk"],
)


@app.get("/")
def home():
    return {"message": "AI Hedge Fund API Running"}