import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.routes import generate_meme
from app.models.meme_request import MemeRequest

@pytest.mark.asyncio
@patch("app.routes.generate_meme.db")
async def test_generate_meme_prisma(mock_db):
    """Test meme generation using mocked Prisma client."""
    # Mock Prisma create return value
    mock_job = MagicMock()
    mock_job.id = "prisma-job-123"
    mock_job.status = "queued"
    
    # Needs to be awaitable
    mock_db.job.create = AsyncMock(return_value=mock_job)

    request = MemeRequest(user_id="test-user")
    response = await generate_meme.generate_meme(request)

    assert response.job_id == "prisma-job-123"
    assert response.status == "queued"
    mock_db.job.create.assert_called_once()
