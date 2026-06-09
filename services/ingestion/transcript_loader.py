import os

from datetime import datetime

from shared.configs.database import SessionLocal
from shared.schemas.raw_documents import RawDocument


TRANSCRIPT_DIR = "data/rag/earnings_calls"


def load_transcripts():

    db = SessionLocal()

    files = [
        f
        for f in os.listdir(TRANSCRIPT_DIR)
        if f.endswith(".txt")
    ]

    print(f"Found {len(files)} transcripts")

    for file_name in files:

        file_path = os.path.join(
            TRANSCRIPT_DIR,
            file_name
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        parts = file_name.replace(".txt", "").split("_")

        ticker = parts[0]
        quarter = parts[1]
        year = parts[2]

        db.add(
            RawDocument(
                ticker=ticker,
                quarter=quarter,
                year=year,
                filing_type="transcript",
                source="earnings_call",
                content=content,
                processed=False,
                created_at=datetime.utcnow()
            )
        )

        print(
            f"Loaded {file_name}"
        )

    db.commit()

    db.close()

    print("All transcripts loaded")
    

if __name__ == "__main__":
    load_transcripts()