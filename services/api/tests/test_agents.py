from unittest.mock import patch, MagicMock
from app.agents import humor_engine, moment_detector

def test_humor_engine_no_key():
    """Test humor engine returns fallback if no key set."""
    with patch("app.core.config.settings.GOOGLE_API_KEY", ""):
        captions = humor_engine.generate_captions({})
        assert "No API Key" in captions[0]

def test_moment_detector_no_key():
    """Test moment detector returns fallback if no key set."""
    with patch("app.core.config.settings.GOOGLE_API_KEY", ""):
        result = moment_detector.detect_moment("dummy_path")
        assert "stub" in result["tags"]

@patch("app.agents.humor_engine.genai")
def test_humor_engine_mock_call(mock_genai):
    """Test humor engine calls gemini when key is present."""
    # Mock the response
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '["Funny Caption 1", "Funny Caption 2"]'
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model

    with patch("app.core.config.settings.GOOGLE_API_KEY", "FAKE_KEY"):
        captions = humor_engine.generate_captions({"tags": ["cat"], "mood_score": 0.9})
        
        assert len(captions) == 2
        assert captions[0] == "Funny Caption 1"
        mock_model.generate_content.assert_called_once()
