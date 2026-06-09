import pandas as pd


def calculate_risk_score(row):

    score = 0

    # Volatility
    score += row.volatility_10 * 100

    # Volume instability
    score += abs(row.volume_change) * 10

    # Extreme RSI
    if row.rsi_14 > 70:
        score += 5

    if row.rsi_14 < 30:
        score += 5

    return score