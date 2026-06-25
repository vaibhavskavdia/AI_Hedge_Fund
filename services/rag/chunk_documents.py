from datetime import datetime
from langchain_text_splitters import (RecursiveCharacterTextSplitter)
from shared.configs.database import SessionLocal
from shared.schemas.raw_documents import RawDocument
from shared.schemas.knowledge_documents import (KnowledgeDocument)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " "
    ]
)


def chunk_documents():

    db = SessionLocal()

    documents = (
        db.query(RawDocument)
        .filter(
            RawDocument.processed == False
        )
        .all()
    )

    print(
        f"Found {len(documents)} documents"
    )

    for doc in documents:

        chunks = splitter.split_text(
            doc.content
        )

        print(
            f"{doc.ticker}: {len(chunks)} chunks"
        )

        for idx, chunk in enumerate(chunks):

            db.add(
                KnowledgeDocument(
                    document_type="transcript_chunk",
                    source=doc.source,
                    title=f"{doc.ticker}_chunk_{idx}",
                    content=chunk,
                    ticker=doc.ticker,
                    quarter=doc.quarter,
                    year=doc.year,
                    created_at=datetime.utcnow()
                )
            )

        doc.processed = True

    db.commit()

    db.close()

    print(
        "Chunking complete"
    )


if __name__ == "__main__":
    chunk_documents()