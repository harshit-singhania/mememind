from typing import Optional
from pydantic import BaseModel

class MemeRequest(BaseModel):
    user_id: str
    mood_hint: str | None = None
    type: str = "image" # "image" or "video"
    media_url: Optional[str] = None
