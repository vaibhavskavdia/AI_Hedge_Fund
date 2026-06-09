from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shared.configs.database import SessionLocal
from shared.schemas.predictions import Prediction
from shared.schemas.apis.predictions import PredictionResponse

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/",
    response_model=list[PredictionResponse]
)
def get_predictions(
    db: Session = Depends(get_db)
):

    predictions = (
        db.query(Prediction)
        .all()
    )

    return predictions


@router.get(
    "/latest",
    response_model=list[PredictionResponse]
)
def get_latest_predictions(
    db: Session = Depends(get_db)
):

    latest_timestamp = (
        db.query(Prediction.timestamp)
        .order_by(Prediction.timestamp.desc())
        .first()
    )

    if not latest_timestamp:
        return []

    predictions = (
        db.query(Prediction)
        .filter(
            Prediction.timestamp == latest_timestamp[0]
        )
        .all()
    )

    return predictions