from sqlalchemy import Column, Integer, String, Float, DateTime

from shared.configs.base import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True)

    prediction_type = Column(String)

    predicted_value = Column(Float)

    confidence = Column(Float)

    created_at = Column(DateTime)

    model_name = Column(String)
    