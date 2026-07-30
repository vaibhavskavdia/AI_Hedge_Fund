import pandas as pd
from sqlalchemy import text

from shared.configs.database import engine
from shared.constants.sector_mapper import SECTOR_MAP


class UniverseBuilder:
    """
    Builds the investable universe from model predictions.

    Responsibilities:
    - Load latest predictions
    - Keep bullish opportunities
    - Attach sector information
    - Return a clean DataFrame

    This class should NOT perform any user-specific filtering.
    That is handled by StockSelector.
    """

    QUERY = """
    SELECT *
    FROM predictions
    ORDER BY prediction_probability DESC;
    """

    def build(self) -> pd.DataFrame:
        """
        Returns the investable universe.

        Returns
        -------
        pd.DataFrame
            Columns:
                ticker
                sector
                prediction_probability
        """

        df = pd.read_sql(
            text(self.QUERY),
            engine,
        )

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "ticker",
                    "sector",
                    "prediction_probability",
                ]
            )

        # Keep only bullish predictions
        df = df[
            df["predicted_class"] == 1
        ].copy()

        # Attach sectors
        df["sector"] = df["ticker"].map(
            SECTOR_MAP
        )

        # Remove unknown sectors
        df = df.dropna(
            subset=["sector"]
        )

        # Highest confidence first
        df = df.sort_values(
            by="prediction_probability",
            ascending=False,
        )

        return df[
            [
                "ticker",
                "sector",
                "prediction_probability",
            ]
        ].reset_index(drop=True)


if __name__ == "__main__":

    builder = UniverseBuilder()

    universe = builder.build()

    print("\nInvestable Universe:\n")
    print(universe.head(50))