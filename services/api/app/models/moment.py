from typing import List
from pydantic import BaseModel

class Moment(BaseModel):
    timestamp: float
    tags: List[str]
    mood_score: float
