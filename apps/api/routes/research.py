from fastapi import APIRouter
from agents.research_agent import ResearchAgent
from services.rag.memory import (save_memory,get_recent_memories)

router = APIRouter(prefix="/research",tags=["Research"])

agent = ResearchAgent()


@router.post("/")
def research(payload: dict):

    question = payload["question"]
    report = agent.answer(question)

    # Save research to memory
    save_memory(agent_name="research_agent",memory_key=question,memory_value=report)
    return {"question": question,"answer": report}


@router.get("/history")

def research_history():
    memories = get_recent_memories(agent_name="research_agent",limit=20)
    return [{"question": memory.memory_key,"answer": memory.memory_value,"created_at": str(memory.created_at)}for memory in memories]