from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from shared.configs.base import Base


class DocumentEmbedding(Base):

    __tablename__ = "document_embeddings"

    id = Column(
        Integer,
        primary_key=True
    )

    document_id = Column(Integer)

    vector_id = Column(String)

    embedding_model = Column(String)

    created_at = Column(DateTime)