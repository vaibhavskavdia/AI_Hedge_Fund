from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from shared.configs.base import Base


class AgentMemory(Base):

    __tablename__ = "agent_memory"

    id = Column(
        Integer,
        primary_key=True
    )

    agent_name = Column(String)

    memory_key = Column(String)

    memory_value = Column(Text)

    created_at = Column(DateTime)