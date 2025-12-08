from fastapi import APIRouter, HTTPException
from app.models.job_status import JobStatus
from app.services.db import db

router = APIRouter()

@router.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    job = await db.job.find_unique(where={"id": job_id})
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return JobStatus(job_id=job.id, status=job.status, result_url=job.result_url)
