# import uuid
from fastapi import APIRouter
from app.models.meme_request import MemeRequest
from app.models.job_status import JobStatus
from app.services.db import db

router = APIRouter()

@router.post("/generate-meme", response_model=JobStatus)
async def generate_meme(request: MemeRequest):
    # Create valid job entry using Prisma
    job = await db.job.create({
        "user_id": request.user_id,
        "status": "queued"
    })
    
    # Trigger background worker (still stubbed)
    # worker.process_job.delay(job.id, request)

    return JobStatus(job_id=job.id, status=job.status)
