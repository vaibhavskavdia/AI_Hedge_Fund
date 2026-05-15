import pandas as pd

from sqlalchemy import text

from shared.configs.database import engine
from sqlalchemy.orm import Session

from shared.schemas.features import FeatureStore

from shared.configs.database import SessionLocal

QUERY = """
SELECT *
FROM stock_prices
WHERE ticker = 'AAPL'
ORDER BY timestamp;
"""


df = pd.read_sql(
    text(QUERY),
    engine
)


# Daily Returns
df["returns"] = df["close"].pct_change()


# Simple Moving Average
df["sma_10"] = df["close"].rolling(window=10).mean()


# Exponential Moving Average
df["ema_10"] = df["close"].ewm(span=10).mean()


# Volatility
df["volatility_10"] = (
    df["returns"]
    .rolling(window=10)
    .std()
)


# Lag Features
df["lag_1"] = df["close"].shift(1)

df["lag_2"] = df["close"].shift(2)
# Target Variable
df["target"] = (
    df["close"].shift(-1)
    > df["close"]
).astype(int)
df = df.dropna()


print(df.head(15))

def store_features(df):

    db: Session = SessionLocal()

    try:

        for _, row in df.iterrows():

            feature_entry = FeatureStore(

                ticker=row["ticker"],

                timestamp=row["timestamp"],

                returns=float(row["returns"]),

                sma_10=float(row["sma_10"]),

                ema_10=float(row["ema_10"]),

                volatility_10=float(
                    row["volatility_10"]
                ),

                lag_1=float(row["lag_1"]),

                lag_2=float(row["lag_2"]),

                target=int(row["target"])
            )

            db.add(feature_entry)

        db.commit()

        print("Features stored successfully!")

    except Exception as e:

        db.rollback()

        print(e)

    finally:

        db.close()
        
store_features(df)
print("Feature engineering completed and stored in database!")