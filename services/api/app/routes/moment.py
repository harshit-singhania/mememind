from fastapi import APIRouter
from app.models.moment import Moment

router = APIRouter()

@router.post("/moment/detect", response_model=Moment)
async def detect_moment():
    # Stub: Return a mock moment
    return Moment(
        timestamp=1234567890.0,
        tags=["mock", "stub"],
        mood_score=0.8
    )
