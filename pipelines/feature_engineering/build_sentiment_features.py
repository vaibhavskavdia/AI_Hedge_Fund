import pandas as pd
from sqlalchemy import text

from shared.configs.database import engine

QUERY = """
SELECT
    ticker,
    DATE(timestamp) as sentiment_date,
    AVG(score) as avg_sentiment,
    COUNT(*) as news_count
FROM news_sentiment
GROUP BY ticker, DATE(timestamp)
ORDER BY sentiment_date;
"""

df = pd.read_sql(text(QUERY), engine)

print(df.head())

print("\nRows:", len(df))
