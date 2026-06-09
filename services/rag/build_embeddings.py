import os
from datetime import datetime

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from pinecone import Pinecone

from shared.configs.database import SessionLocal

from shared.schemas.knowledge_documents import KnowledgeDocument
from shared.schemas.document_embeddings import DocumentEmbedding


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

EMBED_BATCH_SIZE = 64
UPSERT_BATCH_SIZE = 100


def build_embeddings():

    db = SessionLocal()

    existing_embeddings = (
        db.query(DocumentEmbedding)
        .count()
    )

    if existing_embeddings > 0:

        print(
            f"Embeddings already exist: {existing_embeddings}"
        )

        db.close()
        return

    documents = (
        db.query(KnowledgeDocument)
        .all()
    )

    print(
        f"Found {len(documents)} knowledge documents"
    )

    if len(documents) == 0:

        print("No documents found")

        db.close()
        return

    print("Loading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print("Connecting to Pinecone...")

    pc = Pinecone(
        api_key=PINECONE_API_KEY
    )

    index = pc.Index(
        PINECONE_INDEX
    )

    print("Generating embeddings...")

    texts = [
        doc.content
        for doc in documents
    ]

    embeddings = model.encode(
        texts,
        batch_size=EMBED_BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print(
        f"Generated {len(embeddings)} embeddings"
    )

    vectors = []

    embedding_rows = []

    for doc, embedding in zip(
        documents,
        embeddings
    ):

        vector_id = f"doc_{doc.id}"

        metadata = {
            "document_id": doc.id,
            "ticker": doc.ticker,
            "quarter": doc.quarter,
            "year": doc.year,
            "source": doc.source,
            "title": doc.title
        }

        vectors.append(
            (
                vector_id,
                embedding.tolist(),
                metadata
            )
        )

        embedding_rows.append(
            DocumentEmbedding(
                document_id=doc.id,
                vector_id=vector_id,
                embedding_model=MODEL_NAME,
                created_at=datetime.utcnow()
            )
        )

    print("Uploading vectors to Pinecone...")

    for i in range(
        0,
        len(vectors),
        UPSERT_BATCH_SIZE
    ):

        batch = vectors[
            i:i + UPSERT_BATCH_SIZE
        ]

        index.upsert(
            vectors=batch
        )

        print(
            f"Uploaded {min(i + UPSERT_BATCH_SIZE, len(vectors))}/{len(vectors)}"
        )

    print(
        "Saving embedding metadata..."
    )

    db.bulk_save_objects(
        embedding_rows
    )

    db.commit()

    db.close()

    print(
        "Embedding pipeline completed successfully"
    )


if __name__ == "__main__":
    build_embeddings()