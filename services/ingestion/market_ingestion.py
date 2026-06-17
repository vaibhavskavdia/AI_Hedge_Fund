import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from shared.configs.database import SessionLocal
from shared.schemas.stock_prices import StockPrice
from shared.constants.universe import SP500_UNIVERSE

tickers = SP500_UNIVERSE

def fetch_stock_data(ticker: str,period: str = "10y"):

    print(f"Fetching data for {ticker}...")

    stock = yf.Ticker(ticker)

    df = stock.history(period=period)

    return df


def store_stock_data(ticker: str,df: pd.DataFrame):

    db: Session = SessionLocal()

    try:

        for index, row in df.iterrows():

            stock_entry = StockPrice(ticker=ticker,timestamp=index.to_pydatetime(),open=float(row["Open"]),
                                     high=float(row["High"]),low=float(row["Low"]),close=float(row["Close"]),volume=float(row["Volume"])
            )

            db.add(stock_entry)

        db.commit()

        print(f"Stored data for {ticker}")

    except Exception as e:

        db.rollback()

        print("Error storing data:", e)

    finally:

        db.close()


if __name__ == "__main__":
    
    for ticker in tickers:

        data = fetch_stock_data(ticker)

        store_stock_data(ticker, data)