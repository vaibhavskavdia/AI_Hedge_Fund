from pathlib import Path
from datetime import datetime

from shared.configs.database import SessionLocal
from shared.schemas.raw_documents import RawDocument


RAG_FOLDER = Path("data/rag/earnings_calls")


def load_knowledge():

    db = SessionLocal()

    existing_files = {row.file_path for row in db.query(RawDocument.file_path).all()}
    txt_files = list(RAG_FOLDER.glob("*.txt"))
    print(f"Found {len(txt_files)} transcript files")
    added = 0
    skipped = 0
    for file in txt_files:
        file_path = str(file)
        if file_path in existing_files:
            skipped += 1
            continue
        content = file.read_text(encoding="utf-8",errors="ignore")
        ticker = file.stem.upper()
        document = RawDocument(
            ticker=ticker,
            filing_type="earnings_call",
            filing_date=None,
            source_url=None,
            file_path=file_path,
            processed=False,
            source="earnings_call",
            content=content,
            quarter="Q1",
            year="2026",
            created_at=datetime.utcnow()
        )

        db.add(document)
        added += 1

    db.commit()
    db.close()

    print(f"Added {added} new transcripts")
    print(f"Skipped {skipped} existing transcripts")


if __name__ == "__main__":
    load_knowledge()