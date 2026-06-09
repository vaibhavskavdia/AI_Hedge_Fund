import joblib
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from shared.configs.database import engine
from shared.configs.database import SessionLocal
from shared.schemas.predictions import Prediction

MODEL_PATH = "ml/models/artifacts/xgboost_model.pkl"

FEATURE_COLUMNS = ["returns","sma_10","ema_10","volatility_10","lag_1","lag_2","rsi_14","macd",
                   "macd_signal","bb_upper","bb_lower","volume_ma_10","volume_change","avg_sentiment_score",
                   "positive_count","negative_count","neutral_count"]

QUERY = """
SELECT *
FROM feature_store
ORDER BY timestamp DESC;
"""

df = pd.read_sql(text(QUERY), engine)

latest_features = (df.groupby("ticker").head(1))

model = joblib.load(MODEL_PATH)

X = latest_features[FEATURE_COLUMNS]

probs = model.predict_proba(X)[:, 1]

db: Session = SessionLocal()

for i, row in latest_features.iterrows():

    prob = float(probs[list(latest_features.index).index(i)])

    pred_class = int(prob >= 0.5)

    prediction = Prediction(ticker=row["ticker"],prediction_probability=prob,predicted_class=pred_class,timestamp=row["timestamp"])

    db.add(prediction)

db.commit()
db.close()

print("Predictions stored successfully!")