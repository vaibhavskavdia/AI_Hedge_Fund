from sqlalchemy import func

from shared.configs.database import SessionLocal

from shared.schemas.news_sentiment import NewsSentiment
from shared.schemas.news_features import NewsFeature

from logger import logger


def generate_news_features():

    logger.info(
        "Generating news features"
    )

    db = SessionLocal()

    db.query(
        NewsFeature
    ).delete()

    tickers = (
        db.query(
            NewsSentiment.ticker
        )
        .distinct()
        .all()
    )

    total_rows = 0

    for ticker_row in tickers:

        ticker = ticker_row[0]

        rows = (
            db.query(
                NewsSentiment
            )
            .filter(
                NewsSentiment.ticker == ticker
            )
            .all()
        )

        if len(rows) == 0:
            continue

        avg_score = (
            sum(r.score for r in rows)
            / len(rows)
        )

        positive_count = sum(
            1
            for r in rows
            if r.sentiment == "positive"
        )

        negative_count = sum(
            1
            for r in rows
            if r.sentiment == "negative"
        )

        neutral_count = sum(
            1
            for r in rows
            if r.sentiment == "neutral"
        )

        feature = NewsFeature(
            ticker=ticker,
            timestamp=max(
                r.timestamp
                for r in rows
            ),
            avg_sentiment_score=avg_score,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count
        )

        db.add(feature)

        total_rows += 1

    db.commit()

    db.close()

    logger.info(
        f"Created {total_rows} news feature rows"
    )


if __name__ == "__main__":
    generate_news_features()