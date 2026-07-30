from fastapi import APIRouter
from agents.research_agent import ResearchAgent
from services.rag.memory import (save_memory,get_recent_memories)
from apps.api.schemas.requests.research_request import ResearchRequest
from apps.api.schemas.responses.research_response import ResearchResponse

router = APIRouter(prefix="/research",tags=["Research"])

agent = ResearchAgent()


@router.post(
    "/",
    response_model=ResearchResponse,
)
def research(request: ResearchRequest):

    report = agent.answer(request.question)

    save_memory(
        agent_name="research_agent",
        memory_key=request.question,
        memory_value=report,
    )

    return ResearchResponse(
        question=request.question,
        answer=report,
    )


@router.get("/history")

def research_history():
    memories = get_recent_memories(agent_name="research_agent",limit=20)
    return [{"question": memory.memory_key,"answer": memory.memory_value,"created_at": str(memory.created_at)}for memory in memories]