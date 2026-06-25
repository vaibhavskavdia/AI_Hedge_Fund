import joblib
import pandas as pd
import numpy as np
from sqlalchemy import text

from xgboost import XGBRegressor

from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from shared.configs.database import engine


QUERY = """
SELECT *
FROM feature_store
"""


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
]


TARGET = "future_return_5d"


def load_data():

    df = pd.read_sql(
        text(QUERY),
        engine
    )

    df = df.dropna(
        subset=FEATURE_COLUMNS + [TARGET]
    )

    print(f"\nDataset Shape: {df.shape}")

    return df


def train_model():

    df = load_data()

    X = df[FEATURE_COLUMNS]
    y = df[TARGET]

    tscv = TimeSeriesSplit(
        n_splits=5
    )

    mae_scores = []
    rmse_scores = []
    r2_scores = []

    fold = 1

    for train_idx, test_idx in tscv.split(X):

        print(f"\n{'=' * 50}")
        print(f"Fold {fold}")
        print(f"{'=' * 50}")

        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        model = XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train,y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test,predictions)

       

        rmse = np.sqrt(mean_squared_error(y_test,predictions))

        r2 = r2_score(y_test,predictions)

        mae_scores.append(mae)
        rmse_scores.append(rmse)
        r2_scores.append(r2)

        print(f"MAE  : {mae:.6f}")
        print(f"RMSE : {rmse:.6f}")
        print(f"R2   : {r2:.6f}")

        fold += 1

    print("\n")
    print("=" * 60)
    print("Cross Validation Results")
    print("=" * 60)

    print(f"Mean MAE  : {sum(mae_scores) / len(mae_scores):.6f}")
    print(f"Mean RMSE : {sum(rmse_scores) / len(rmse_scores):.6f}")
    print(f"Mean R2   : {sum(r2_scores) / len(r2_scores):.6f}")

    print("\nTraining final model on full dataset...")

    final_model = XGBRegressor(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    final_model.fit(X,y)

    joblib.dump(final_model,"ml/models/artifacts/return_forecaster.pkl")

    print("\nReturn forecaster saved successfully!")


if __name__ == "__main__":

    train_model()