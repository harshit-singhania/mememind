"""
Agent responsible for analyzing images/video to detect key moments.
"""
import time
import json
import google.generativeai as genai
from app.core.config import settings

def detect_moment(file_path: str) -> dict:
    """
    Analyzes the file at file_path using Gemini Vision.
    """
    if not settings.GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY not set. Returning stub data.")
        return {
            "timestamp": time.time(),
            "tags": ["stub", "missing_key"],
            "mood_score": 0.5
        }

    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')

        from PIL import Image
        with Image.open(file_path) as image_data:
            prompt = "Analyze this image. Return a JSON object with keys: 'tags' (list of strings, max 5 relevant tags), 'mood_score' (float 0.0 to 1.0, where 1.0 Is very intense/funny/emotional)."
            
            response = model.generate_content([prompt, image_data])
            text = response.text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(text)
        
        # Validate structure
        if "tags" not in result: result["tags"] = ["meme"]
        if "mood_score" not in result: result["mood_score"] = 0.5
        
        result["timestamp"] = time.time()
        return result

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {
            "timestamp": time.time(),
            "tags": ["error", "gemini_fail"],
            "mood_score": 0.0
        }
