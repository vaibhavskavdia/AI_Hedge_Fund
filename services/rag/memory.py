from datetime import datetime,UTC
from shared.configs.database import SessionLocal
from shared.schemas.agent_memory import AgentMemory

def save_memory(agent_name,memory_key,memory_value):

    db = SessionLocal()
    db.add(AgentMemory(agent_name=agent_name,memory_key=memory_key,memory_value=memory_value,created_at=datetime.now(UTC)))
    db.commit()
    db.close()
    
def get_memory(agent_name,memory_key):
    db = SessionLocal()
    memories = (db.query(AgentMemory).filter(AgentMemory.agent_name == agent_name,AgentMemory.memory_key == memory_key).all())
    db.close()
    return [memory.memory_value for memory in memories]

def get_recent_memories(agent_name,limit=10):
    db = SessionLocal()
    memories = (db.query(AgentMemory).filter(AgentMemory.agent_name == agent_name).order_by(AgentMemory.created_at.desc()).limit(limit).all())
    db.close()
    return memories

if __name__ == "__main__":

    save_memory(agent_name="research_agent",memory_key="tesla_ai",memory_value="Tesla is investing heavily in AI.")

    memories = get_memory("research_agent","tesla_ai")

    print(memories)