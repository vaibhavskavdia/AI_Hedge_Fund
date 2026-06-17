import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.configs.database import engine
from shared.configs.database import SessionLocal
from shared.schemas.features import FeatureStore
from shared.schemas.news_features import NewsFeature

QUERY = """
SELECT *
FROM stock_prices
ORDER BY timestamp;
"""

df = pd.read_sql(text(QUERY),engine)
spy_df = (df[df["ticker"] == "SPY"].copy().sort_values("timestamp"))
spy_df["spy_return"] = (spy_df["close"].pct_change())
spy_lookup = spy_df[[    "timestamp",    "spy_return"]]
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
    gain = delta.where(delta > 0,0)
    loss = -delta.where(delta < 0,0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    ticker_df["rsi_14"] = (100 - (100 / (1 + rs)))
    # MACD
    ema_12 = (ticker_df["close"].ewm(span=12).mean())
    ema_26 = (ticker_df["close"].ewm(span=26).mean())
    ticker_df["macd"] = (ema_12 - ema_26)
    ticker_df["macd_signal"] = (ticker_df["macd"].ewm(span=9).mean())
    # Bollinger
    ticker_df["bb_middle"] = (ticker_df["close"].rolling(window=20).mean())
    bb_std = (ticker_df["close"].rolling(window=20).std())
    ticker_df["bb_upper"] = (ticker_df["bb_middle"]+ 2 * bb_std)
    ticker_df["bb_lower"] = (ticker_df["bb_middle"]- 2 * bb_std)
    # Volume
    ticker_df["volume_ma_10"] = (ticker_df["volume"].rolling(window=10).mean())
    ticker_df["volume_change"] = (ticker_df["volume"].pct_change())
    ticker_df["volume_spike"] = (ticker_df["volume"]/ticker_df["volume"].rolling(20).mean())
    # 52 WEEK FEATURES
    ticker_df["high_52w"] = (ticker_df["close"].rolling(252).max())
    ticker_df["dist_52w_high"] = (ticker_df["close"]/ticker_df["high_52w"])
    ticker_df["low_52w"] = (ticker_df["close"].rolling(252).min())
    ticker_df["dist_52w_low"] = (ticker_df["close"]/ticker_df["low_52w"])

    # SPY RELATIVE STRENGTH
    ticker_df = ticker_df.merge(spy_lookup,on="timestamp",how="left")
    ticker_df["relative_strength"] = (ticker_df["returns"]-ticker_df["spy_return"])
    # Lag Features
    ticker_df["lag_1"] = (ticker_df["close"].shift(1))
    ticker_df["lag_2"] = (ticker_df["close"].shift(2))
    # Target
    future_return_5d = (ticker_df["close"].shift(-5)/ticker_df["close"]- 1)
    ticker_df["target"] = (future_return_5d > 0.010).astype(int)
    ticker_df = ticker_df.dropna()
    all_features.append(ticker_df)

df = pd.concat(all_features,ignore_index=True)
print(df.head())

def store_features(df):

    db: Session = SessionLocal()
    db.query(FeatureStore).delete()

    try:

        sentiment_lookup = {}
        news_features = db.query(NewsFeature).all()

        for news in news_features:
            sentiment_lookup[news.ticker] = news
        
        for _, row in df.iterrows():
            news = sentiment_lookup.get(row["ticker"])
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
                volume_spike=float(row["volume_spike"]),
                relative_strength=float(row["relative_strength"]),
                dist_52w_high=float(row["dist_52w_high"]),
                dist_52w_low=float(row["dist_52w_low"]),
                lag_1=float(row["lag_1"]),
                lag_2=float(row["lag_2"]),
                avg_sentiment_score=(float(news.avg_sentiment_score)if news else 0.0),
                positive_count=(int(news.positive_count)if news else 0),
                negative_count=(int(news.negative_count)if news else 0),
                neutral_count=(int(news.neutral_count)if news else 0),
                target=int(row["target"]))

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