import threading
import uuid


_jobs = {}

_lock = threading.Lock()


def create_job():

    job_id = str(uuid.uuid4())

    with _lock:

        _jobs[job_id] = {
            "status": "running",
            "progress": 0,
            "step": "Initializing...",
            "portfolio_id": None,
            "error": None,
        }

    return job_id


def update_job(
    job_id,
    *,
    progress=None,
    step=None,
    status=None,
    portfolio_id=None,
    error=None,
):

    with _lock:

        if job_id not in _jobs:
            return

        job = _jobs[job_id]

        if progress is not None:
            job["progress"] = progress

        if step is not None:
            job["step"] = step

        if status is not None:
            job["status"] = status

        if portfolio_id is not None:
            job["portfolio_id"] = portfolio_id

        if error is not None:
            job["error"] = str(error)


def get_job(job_id):

    with _lock:
        return _jobs.get(job_id)