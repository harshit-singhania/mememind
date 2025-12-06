import uuid
from fastapi import APIRouter
from app.models.meme_request import MemeRequest
from app.models.job_status import JobStatus
from app.services.supabase_client import SupabaseClient

router = APIRouter()

@router.post("/generate-meme", response_model=JobStatus)
async def generate_meme(request: MemeRequest):
    job_id = str(uuid.uuid4())
    supabase = SupabaseClient()
    
    # Create valid job entry in DB
    job_data = supabase.create_job(job_id, request.user_id)
    
    # Trigger background worker (still stubbed)
    # worker.process_job.delay(job_id, request)

    return JobStatus(job_id=job_id, status=job_data.get("status", "queued"))
