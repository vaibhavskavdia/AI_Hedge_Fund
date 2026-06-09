from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Boolean,
    Text
)

from shared.configs.base import Base


class RawDocument(Base):

    __tablename__ = "raw_documents"

    id = Column(
        Integer,
        primary_key=True
    )

    ticker = Column(String)

    filing_type = Column(String)

    filing_date = Column(Date)

    source_url = Column(Text)

    file_path = Column(Text)

    processed = Column(Boolean)

    source = Column(String(50))
    
    content = Column(Text)
    
    quarter = Column(String(10))

    year = Column(String(10))
    
    created_at = Column(DateTime)