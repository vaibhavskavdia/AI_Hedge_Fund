from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    ticker: str
    prediction_probability: float
    predicted_class: int
    timestamp: datetime

    class Config:
        from_attributes = True