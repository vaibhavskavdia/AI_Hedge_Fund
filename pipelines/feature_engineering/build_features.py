import pandas as pd
from sqlalchemy import text
from shared.configs.database import engine
from sqlalchemy.orm import Session
from shared.schemas.features import FeatureStore
from shared.configs.database import SessionLocal

QUERY = """
SELECT *
FROM stock_prices
ORDER BY timestamp;
"""

df = pd.read_sql(text(QUERY),engine)
all_features = []

for ticker in df["ticker"].unique():

    ticker_df = (df[df["ticker"] == ticker].copy().sort_values("timestamp"))
    # Returns
    ticker_df["returns"] = (ticker_df["close"].pct_change())
    
    # SMA
    ticker_df["sma_10"] = (ticker_df["close"].rolling(window=10).mean())
    
    # EMA
    ticker_df["ema_10"] = (ticker_df["close"].ewm(span=10).mean())
    
    # Volatility
    ticker_df["volatility_10"] = (ticker_df["returns"].rolling(window=10).std())
    
    # RSI
    delta = ticker_df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    ticker_df["rsi_14"] = (100 - (100 / (1 + rs)))
    
    # MACD
    ema_12 = (ticker_df["close"].ewm(span=12).mean())
    ema_26 = (ticker_df["close"].ewm(span=26).mean())
    ticker_df["macd"] = ema_12 - ema_26
    ticker_df["macd_signal"] = (ticker_df["macd"].ewm(span=9).mean())
    
    # Bollinger
    ticker_df["bb_middle"] = (ticker_df["close"].rolling(window=20).mean())
    bb_std = (ticker_df["close"].rolling(window=20).std())
    ticker_df["bb_upper"] = (ticker_df["bb_middle"]+ 2 * bb_std)
    ticker_df["bb_lower"] = (ticker_df["bb_middle"]- 2 * bb_std)
    
    # Volume
    ticker_df["volume_ma_10"] = (ticker_df["volume"].rolling(window=10).mean())
    ticker_df["volume_change"] = (ticker_df["volume"].pct_change())
    
    # Lag Features
    ticker_df["lag_1"] = (ticker_df["close"].shift(1))
    ticker_df["lag_2"] = (ticker_df["close"].shift(2))
    
    # Target
    ticker_df["target"] = (ticker_df["close"].shift(-1)> ticker_df["close"]).astype(int)
    ticker_df = ticker_df.dropna()

    all_features.append(ticker_df)

df = pd.concat(all_features,ignore_index=True)
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
                volatility_10=float(row["volatility_10"]),
                rsi_14=float(row["rsi_14"]),
                macd=float(row["macd"]),
                macd_signal=float(row["macd_signal"]),
                bb_upper=float(row["bb_upper"]),
                bb_lower=float(row["bb_lower"]),
                volume_ma_10=float(row["volume_ma_10"]),
                volume_change=float(row["volume_change"]),
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