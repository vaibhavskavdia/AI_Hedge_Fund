from datetime import datetime
import os

from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

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

    try:

        # Get already embedded document IDs
        embedded_doc_ids = [
            row[0]
            for row in db.query(DocumentEmbedding.document_id).all()
        ]

        # Only fetch documents not yet embedded
        if len(embedded_doc_ids) > 0:
            documents = (
                db.query(KnowledgeDocument)
                .filter(~KnowledgeDocument.id.in_(embedded_doc_ids))
                .all()
            )
        else:
            documents = db.query(KnowledgeDocument).all()

        print(f"Found {len(documents)} NEW documents to embed")

        if len(documents) == 0:
            print("No new documents found")
            return

        print("Loading embedding model...")
        model = SentenceTransformer(MODEL_NAME)

        print("Connecting to Pinecone...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX)

        texts = [doc.content for doc in documents]

        print("Generating embeddings...")
        embeddings = model.encode(
            texts,
            batch_size=EMBED_BATCH_SIZE,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(f"Generated {len(embeddings)} embeddings")

        vectors = []
        embedding_rows = []

        for doc, embedding in zip(documents, embeddings):

            vector_id = f"doc_{doc.id}"

            metadata = {
    "document_id": int(doc.id),
    "ticker": str(doc.ticker or ""),
    "quarter": str(doc.quarter or ""),
    "year": str(doc.year or ""),
    "source": str(doc.source or ""),
    "title": str(doc.title or "")
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

        for i in range(0, len(vectors), UPSERT_BATCH_SIZE):

            batch = vectors[i:i + UPSERT_BATCH_SIZE]

            index.upsert(vectors=batch)

            print(
                f"Uploaded {min(i + UPSERT_BATCH_SIZE, len(vectors))}/{len(vectors)}"
            )

        print("Saving embedding metadata...")

        db.bulk_save_objects(embedding_rows)

        db.commit()

        print("Embedding pipeline completed successfully")

    except Exception as e:

        db.rollback()

        print(f"ERROR: {e}")

    finally:

        db.close()


if __name__ == "__main__":
    build_embeddings()