from shared.configs.database import engine
from shared.configs.base import Base

from shared.schemas.stock_prices import StockPrice
from shared.schemas.news import NewsArticle
from shared.schemas.predictions import Prediction
from shared.schemas.features import FeatureStore

print("Creating database tables...")


Base.metadata.create_all(bind=engine)


print("Tables created successfully!")