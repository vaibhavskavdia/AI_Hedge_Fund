from shared.configs.database import engine
from shared.configs.base import Base

from shared.schemas.stock_prices import StockPrice
#from shared.schemas.news import NewsArticle
from shared.schemas.predictions import Prediction
from shared.schemas.features import FeatureStore
from shared.schemas.news_sentiment import NewsSentiment
from shared.schemas.backtest_predictions import BacktestPrediction
from shared.schemas.portfolio_positions import PortfolioPosition
from shared.schemas.agent_memory import AgentMemory
from shared.schemas.document_embeddings import DocumentEmbedding
from shared.schemas.knowledge_documents import KnowledgeDocument
from shared.schemas.news_articles import NewsArticle
from shared.schemas.news_features import NewsFeature
from shared.schemas.raw_documents import RawDocument
from shared.schemas.portfolio_risk import PortfolioRisk 
from shared.schemas.final_portfolio import FinalPortfolio   
from shared.schemas.portfolio_runs import PortfolioRun
from shared.schemas.ai_recommendation import AIRecommendation
print("Creating database tables...")


Base.metadata.create_all(bind=engine)


print("Tables created successfully!")