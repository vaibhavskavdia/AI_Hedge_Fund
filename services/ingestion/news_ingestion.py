from datetime import datetime

import yfinance as yf

from shared.configs.database import SessionLocal
from shared.schemas.news_articles import NewsArticle

from logger import logger


TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
    "JPM",
    "SPY"
]


def ingest_news():

    logger.info("Starting news ingestion")

    db = SessionLocal()

    total_articles = 0

    try:

        for ticker in TICKERS:

            try:

                logger.info(f"Fetching news for {ticker}")

                stock = yf.Ticker(ticker)

                news_items = stock.news

                if not news_items:
                    logger.warning(
                        f"No news found for {ticker}"
                    )
                    continue

                for item in news_items:

                    content = item.get(
                        "content",
                        {}
                    )

                    published_at = None

                    try:

                        pub_date = content.get(
                            "pubDate"
                        )

                        if pub_date:

                            published_at = (
                                datetime.fromisoformat(
                                    pub_date.replace(
                                        "Z",
                                        "+00:00"
                                    )
                                )
                            )

                    except Exception:

                        published_at = None

                    article = NewsArticle(

                        ticker=ticker,

                        headline=content.get(
                            "title"
                        ),

                        summary=content.get(
                            "summary"
                        ),

                        source=(
                            content.get(
                                "provider",
                                {}
                            ).get(
                                "displayName"
                            )
                        ),

                        url=(
                            content.get(
                                "canonicalUrl",
                                {}
                            ).get(
                                "url"
                            )
                        ),

                        published_at=published_at,

                        created_at=datetime.utcnow()
                    )

                    db.add(article)

                    total_articles += 1

            except Exception as e:

                logger.error(
                    f"{ticker}: {str(e)}"
                )

        db.commit()

        logger.info(
            f"Stored {total_articles} articles"
        )

    finally:

        db.close()


if __name__ == "__main__":

    ingest_news()