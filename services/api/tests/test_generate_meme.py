from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_meme_stub():
    payload = {
        "user_id": "test_user",
        "mood_hint": "funny"
    }
    response = client.post("/generate-meme", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"
