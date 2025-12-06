from unittest.mock import patch, MagicMock
from app.services.supabase_client import SupabaseClient

@patch("app.services.supabase_client.create_client")
def test_supabase_create_job_stub(mock_create):
    """Test fallback when no keys."""
    # Ensure keys are empty so client is None
    with patch("app.core.config.settings.SUPABASE_URL", ""), \
         patch("app.core.config.settings.SUPABASE_SERVICE_KEY", ""):
        client = SupabaseClient()
        result = client.create_job("job-123", "user-1")

    assert result["id"] == "job-123"
    assert result["status"] == "queued"
    mock_create.assert_not_called()

@patch("app.services.supabase_client.create_client")
def test_supabase_create_job_real(mock_create):
    """Test job creation utilizes the supabase client correctly."""
    mock_client = MagicMock()
    mock_create.return_value = mock_client
    
    # Mock insert response
    mock_response = MagicMock()
    mock_response.data = [{"id": "job-123", "status": "queued"}]
    mock_client.table.return_value.insert.return_value.execute.return_value = mock_response

    with patch("app.core.config.settings.SUPABASE_URL", "https://test.supabase.co"), \
         patch("app.core.config.settings.SUPABASE_SERVICE_KEY", "test-key"):
        client = SupabaseClient()
        result = client.create_job("job-123", "user-1")

    assert result["id"] == "job-123"
    assert result["status"] == "queued"
    mock_client.table.assert_called_with("jobs")

@patch("app.services.supabase_client.create_client")
def test_supabase_upload(mock_create):
    """Test media upload calls storage."""
    mock_client = MagicMock()
    mock_create.return_value = mock_client
    
    mock_client.storage.from_.return_value.get_public_url.return_value = "http://fake-url/img.jpg"

    with patch("app.core.config.settings.SUPABASE_URL", "https://test.supabase.co"), \
         patch("app.core.config.settings.SUPABASE_SERVICE_KEY", "test-key"):
        client = SupabaseClient()
        # Create a dummy file for the test
        with open("dummy.jpg", "w") as f:
            f.write("test")
        
        url = client.upload_media("dummy.jpg")
        assert "http://fake-url/img.jpg" in url
    
    # Clean up
    import os
    if os.path.exists("dummy.jpg"):
        os.remove("dummy.jpg")
