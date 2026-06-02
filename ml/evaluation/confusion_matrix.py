import pandas as pd
from sqlalchemy import text
from shared.configs.database import engine

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from xgboost import XGBClassifier

import matplotlib.pyplot as plt

QUERY = """
SELECT *
FROM feature_store
ORDER BY timestamp;
"""

df = pd.read_sql(text(QUERY), engine)

FEATURE_COLUMNS = ["returns","sma_10","ema_10","volatility_10","rsi_14","macd","macd_signal","bb_upper","bb_lower","volume_ma_10","volume_change","lag_1","lag_2"]

X = df[FEATURE_COLUMNS]
y = df["target"]

split_idx = int(len(df) * 0.8)

X_train = X.iloc[:split_idx]
X_test = X.iloc[split_idx:]

y_train = y.iloc[:split_idx]
y_test = y.iloc[split_idx:]

model = XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)

disp.plot()

plt.title("XGBoost Confusion Matrix")

plt.show()