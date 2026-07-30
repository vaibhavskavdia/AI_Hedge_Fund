from pydantic import BaseModel


class JobStatusResponse(BaseModel):
    job_id: str
    status: str

    progress: int | None = None
    step: str | None = None
    portfolio_id: int | None = None

    error: str | None = None