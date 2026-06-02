import pandas as pd
import shap

from sqlalchemy import text
from shared.configs.database import engine

from xgboost import XGBClassifier

QUERY = """
SELECT *
FROM feature_store
ORDER BY timestamp;
"""

df = pd.read_sql(text(QUERY), engine)

FEATURE_COLUMNS = ["returns","sma_10","ema_10","volatility_10","rsi_14","macd","macd_signal","bb_upper","bb_lower","volume_ma_10","volume_change","lag_1","lag_2"]

X = df[FEATURE_COLUMNS]
y = df["target"]

model = XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,random_state=42)

model.fit(X, y)

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

shap.summary_plot(shap_values,X)