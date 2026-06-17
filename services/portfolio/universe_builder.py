import pandas as pd
from sqlalchemy import text

from shared.configs.database import engine
from shared.constants.sector_mapper import SECTOR_MAP

QUERY = """
SELECT *
FROM predictions
ORDER BY prediction_probability DESC;
"""

df = pd.read_sql(
    text(QUERY),
    engine
)

# Keep only bullish predictions
df = df[
    df["predicted_class"] == 1
]

# Attach sectors
df["sector"] = df["ticker"].map(
    SECTOR_MAP
)

# Remove unknown sectors
df = df.dropna(
    subset=["sector"]
)

# Sort by probability
df = df.sort_values(
    "prediction_probability",
    ascending=False
)

# Top opportunities
universe = df[
    [
        "ticker",
        "sector",
        "prediction_probability"
    ]
]

print("\nInvestable Universe:\n")
print(universe.head(50))