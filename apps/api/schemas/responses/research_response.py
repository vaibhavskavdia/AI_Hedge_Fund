from pydantic import BaseModel


class ResearchResponse(BaseModel):
    question: str
    answer: str