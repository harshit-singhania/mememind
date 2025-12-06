from typing import Optional
from pydantic import BaseModel

class MemeRequest(BaseModel):
    user_id: str
    mood_hint: Optional[str] = None
    media_url: Optional[str] = None
