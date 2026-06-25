import pandas as pd
from sqlalchemy import text
from shared.configs.database import engine
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (accuracy_score,classification_report)
from xgboost import XGBClassifier

QUERY = """
SELECT *
FROM feature_store
ORDER BY timestamp;
"""
# Load Feature Store Data
df = pd.read_sql(text(QUERY),engine)

# Feature Columns
FEATURE_COLUMNS = [ 
    "returns",
    "sma_10",
    "ema_10",
    "volatility_10",
    "rsi_14",
    "macd",
    "macd_signal",
    "bb_upper",
    "bb_lower",
    "volume_ma_10",
    "volume_change",
    "volume_spike",
    "relative_strength",
    "dist_52w_high",
    "dist_52w_low",
    "lag_1",
    "lag_2",
    "avg_sentiment_score",
    "positive_count",
    "negative_count",
    "neutral_count"
    ,"future_return_5d"
]
# Inputs and Target
print("Dataframe Shape:", df.shape)
print(df.head())
X = df[FEATURE_COLUMNS]
y = df["target"]
# Time Series Cross Validation
tscv = TimeSeriesSplit(n_splits=5)
accuracies = []

for fold, (train_index, test_index) in enumerate(tscv.split(X),start=1):
    print(f"\nFold {fold}")
    X_train = X.iloc[train_index]
    X_test = X.iloc[test_index]
    y_train = y.iloc[train_index]
    y_test = y.iloc[test_index]
    # Model
    model = XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,random_state=42)
    # Train
    model.fit(X_train,y_train)
    # Predict
    predictions = model.predict(X_test)
    # Accuracy
    accuracy = accuracy_score(y_test,predictions)
    accuracies.append(accuracy)
    print(f"Accuracy: {accuracy:.4f}")
    print(classification_report(y_test,predictions))
# Final Mean Accuracy
mean_accuracy = (sum(accuracies)/ len(accuracies))

print("\nCross Validation Accuracies:")
print(accuracies)
print(f"\nMean Accuracy: "f"{mean_accuracy:.4f}")

import joblib

final_model = XGBClassifier(n_estimators=500,
    max_depth=6,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=5,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1)

final_model.fit(X, y)

joblib.dump(
    final_model,
    "ml/models/artifacts/xgboost_model.pkl"
)

print("Model saved successfully!")