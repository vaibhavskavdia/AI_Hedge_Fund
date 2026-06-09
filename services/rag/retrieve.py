import os

from dotenv import load_dotenv

from pinecone import Pinecone

from sentence_transformers import SentenceTransformer

from shared.configs.database import SessionLocal

from shared.schemas.knowledge_documents import KnowledgeDocument


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5


model = SentenceTransformer(
    MODEL_NAME
)

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    PINECONE_INDEX
)


def retrieve_context(
    query: str,
    top_k: int = TOP_K,
    ticker: str | None = None
):

    query_embedding = model.encode(
        query
    ).tolist()

    search_kwargs = {
        "vector": query_embedding,
        "top_k": top_k,
        "include_metadata": True
    }

    if ticker:

        search_kwargs["filter"] = {
            "ticker": {
                "$eq": ticker
            }
        }

    results = index.query(
        **search_kwargs
    )

    db = SessionLocal()

    retrieved_chunks = []

    for match in results["matches"]:

        document_id = (
            match["metadata"]
            ["document_id"]
        )

        score = match["score"]

        document = (
            db.query(KnowledgeDocument)
            .filter(
                KnowledgeDocument.id
                == document_id
            )
            .first()
        )

        if not document:
            continue

        retrieved_chunks.append(
            {
                "document_id": document.id,
                "ticker": document.ticker,
                "quarter": document.quarter,
                "year": document.year,
                "score": round(score, 4),
                "content": document.content
            }
        )

    db.close()

    return retrieved_chunks


if __name__ == "__main__":

    results = retrieve_context(
        query="Why is Tesla investing heavily in AI?",
        ticker="TSLA"
    )

    print("\nRESULTS\n")

    for idx, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {idx} ---"
        )

        print(
            f"Ticker: {result['ticker']}"
        )

        print(
            f"Quarter: {result['quarter']}"
        )

        print(
            f"Year: {result['year']}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            result["content"]
        )