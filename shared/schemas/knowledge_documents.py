from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from shared.configs.base import Base


class KnowledgeDocument(Base):

    __tablename__ = "knowledge_documents"

    id = Column(
        Integer,
        primary_key=True
    )

    document_type = Column(String)

    source = Column(String)

    title = Column(String)

    content = Column(Text)
    
    ticker = Column(String(20))

    quarter = Column(String(10))

    year = Column(String(10))
    
    created_at = Column(DateTime)