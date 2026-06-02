from sqlalchemy import Column,Integer,String,Float,DateTime
from shared.configs.base import Base

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)

    prediction_probability = Column(Float)

    predicted_class = Column(Integer)

    timestamp = Column(DateTime)
    