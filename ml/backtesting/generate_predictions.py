import pandas as pd
from sqlalchemy import text
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier
from shared.configs.database import engine
from shared.configs.database import SessionLocal
from shared.constants.features import FEATURE_COLUMNS
from shared.schemas.backtest_predictions import BacktestPrediction
from logger import logger

QUERY = """
SELECT *
FROM feature_store
ORDER BY timestamp;
"""

def generate_backtest_predictions():

    logger.info("Loading feature store data")

    df = pd.read_sql(text(QUERY),engine)
    X = df[FEATURE_COLUMNS]
    y = df["target"]
    tscv = TimeSeriesSplit(n_splits=5)
    db = SessionLocal()
    logger.info("Clearing old backtest predictions")

    db.query(BacktestPrediction).delete()
    db.commit()
    total_predictions = 0
    for fold, (train_idx,test_idx) in enumerate(tscv.split(X),start=1):

        logger.info(f"Running Fold {fold}")
        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]
        y_train = y.iloc[train_idx]
        model = XGBClassifier(n_estimators=100,max_depth=4,learning_rate=0.05,random_state=42)
        model.fit(X_train,y_train)
        probabilities = (model.predict_proba(X_test)[:, 1])
        predictions = (probabilities >= 0.5).astype(int)
        test_rows = df.iloc[test_idx]

        for idx, row in enumerate(test_rows.itertuples()):

            prediction = BacktestPrediction(ticker=row.ticker,timestamp=row.timestamp,target=row.target,
                                            prediction_probability=float(probabilities[idx]),predicted_class=int(predictions[idx]),fold=fold)

            db.add(prediction)

            total_predictions += 1

    db.commit()

    db.close()

    logger.info(f"Generated {total_predictions} "f"historical predictions")


if __name__ == "__main__":

    generate_backtest_predictions()