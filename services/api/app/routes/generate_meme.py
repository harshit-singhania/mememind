import uuid
from fastapi import APIRouter
from app.models.meme_request import MemeRequest
from app.models.job_status import JobStatus

router = APIRouter()

@router.post("/generate-meme", response_model=JobStatus)
async def generate_meme(request: MemeRequest):
    # Stub: Create a job ID and return 'queued'
    job_id = str(uuid.uuid4())
    return JobStatus(job_id=job_id, status="queued")
