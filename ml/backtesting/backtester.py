import pandas as pd

from sqlalchemy import text

from shared.configs.database import engine
from logger import logger

from ml.backtesting.metrics import (
    sharpe_ratio,
    max_drawdown,
    win_rate
)

PREDICTIONS_QUERY = """
SELECT *
FROM backtest_predictions;
"""

PRICES_QUERY = """
SELECT
    ticker,
    timestamp,
    close
FROM stock_prices;
"""
def capped_weights(group):

    weights = (
        group["prediction_probability"]
        / group["prediction_probability"].sum()
    )

    weights = weights.clip(upper=0.20)

    weights = weights / weights.sum()

    return weights


def run_backtest():

    logger.info("Loading predictions")

    predictions = pd.read_sql(text(PREDICTIONS_QUERY),engine)

    logger.info("Loading prices")

    prices = pd.read_sql(text(PRICES_QUERY),engine)

    prices = prices.sort_values(["ticker", "timestamp"])

    prices["next_close"] = (prices.groupby("ticker")["close"].shift(-1))

    prices["actual_return"] = ( prices["next_close"] -prices["close"]) / prices["close"]

    # SPY benchmark

    spy_df = prices[prices["ticker"] == "SPY"].copy()
    spy_df = spy_df.dropna(subset=["actual_return"])

    spy_daily = spy_df[["timestamp", "actual_return"]].copy()

    spy_daily = spy_daily.sort_values("timestamp")

    spy_daily["spy_equity_curve"] = (1 +spy_daily["actual_return"]).cumprod()

    spy_total_return = (spy_daily["spy_equity_curve"].iloc[-1]- 1)

    spy_sharpe = sharpe_ratio(spy_daily["actual_return"])

    spy_drawdown = max_drawdown(spy_daily["spy_equity_curve"])
    
    prices = prices[["ticker", "timestamp", "actual_return"]]

    logger.info("Merging predictions and returns")

    df = predictions.merge(prices,on=["ticker", "timestamp"],how="inner")

    df = df.dropna()

    logger.info(f"Merged rows: {len(df)}")

    # Long signals only

    trades = df[df["predicted_class"] == 1].copy()

    logger.info(f"Total long signals: {len(trades)}")

# Probability weighted portfolio


    trades["weight"] = (trades.groupby("timestamp", group_keys=False).apply(capped_weights))
    
    trades["weighted_return"] = (trades["weight"]* trades["actual_return"])
    
    daily_returns = (trades.groupby("timestamp")["weighted_return"].sum().reset_index())

    daily_returns.rename(columns={"weighted_return":"portfolio_return"},inplace=True)

    daily_returns.rename(columns={"actual_return":"portfolio_return"},inplace=True)

    # Equity curve

    daily_returns["equity_curve"] = (1 +daily_returns["portfolio_return"]).cumprod()

    total_return = (daily_returns["equity_curve"].iloc[-1]- 1)

    sharpe = sharpe_ratio(daily_returns["portfolio_return"])

    drawdown = max_drawdown(daily_returns["equity_curve"])

    winrate = win_rate(daily_returns["portfolio_return"])

    print("\n========== BACKTEST ==========")

    print(f"Total Return: {total_return:.2%}")

    print(f"Sharpe Ratio: {sharpe:.4f}")

    print(f"Max Drawdown: {drawdown:.2%}")

    print(f"Win Rate: {winrate:.2%}")

    logger.info(f"Total Return: {total_return:.4f}")

    logger.info(f"Sharpe Ratio: {sharpe:.4f}")

    logger.info(f"Max Drawdown: {drawdown:.4f}")

    logger.info(f"Win Rate: {winrate:.4f}")
    
    print("\n========== SPY BENCHMARK ==========")

    print(f"SPY Return: {spy_total_return:.2%}")

    print(f"SPY Sharpe: {spy_sharpe:.4f}")

    print(f"SPY Max Drawdown: {spy_drawdown:.2%}")
    
    alpha = (total_return -spy_total_return)
    
    print(f"Alpha vs SPY: {alpha:.2%}")

    return daily_returns


if __name__ == "__main__":

    run_backtest()