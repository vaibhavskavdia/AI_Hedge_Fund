from datetime import datetime

from shared.configs.database import SessionLocal
from shared.schemas.knowledge_documents import KnowledgeDocument


def load_knowledge():

    db = SessionLocal()

    documents = [

        {
            "document_type": "company_research",
            "source": "manual",
            "title": "Apple Business Overview",
            "content": """
Apple Inc designs consumer electronics,
software and cloud services.

Major revenue sources:
- iPhone
- Mac
- iPad
- Services
- Wearables

Strengths:
Strong brand loyalty
Large ecosystem
Recurring services revenue

Risks:
Dependence on iPhone sales
China exposure
Regulatory pressure
"""
        },

        {
            "document_type": "company_research",
            "source": "manual",
            "title": "Microsoft Business Overview",
            "content": """
Microsoft operates across:

- Azure Cloud
- Office 365
- Windows
- Gaming
- AI

Strengths:
Enterprise dominance
Cloud growth
Strong balance sheet

Risks:
Cloud competition
Regulatory pressure
"""
        },

        {
            "document_type": "market_research",
            "source": "manual",
            "title": "General Market Risk Factors",
            "content": """
Stock markets are affected by:

Interest rates
Inflation
Economic growth
Geopolitical events
Corporate earnings

Higher interest rates often reduce growth stock valuations.
"""
        }

    ]

    db.query(KnowledgeDocument).delete()

    for doc in documents:

        db.add(
            KnowledgeDocument(
                document_type=doc["document_type"],
                source=doc["source"],
                title=doc["title"],
                content=doc["content"],
                created_at=datetime.utcnow()
            )
        )

    db.commit()
    db.close()

    print("Knowledge documents loaded successfully")


if __name__ == "__main__":
    load_knowledge()