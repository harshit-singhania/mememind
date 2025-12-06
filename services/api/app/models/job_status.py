from typing import Optional
from pydantic import BaseModel

class JobStatus(BaseModel):
    job_id: str
    status: str
    result_url: Optional[str] = None
