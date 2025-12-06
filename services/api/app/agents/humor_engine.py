"""
Agent responsible for generating captions and humor.
"""
import google.generativeai as genai
from app.core.config import settings
import json

def generate_captions(moment: dict) -> list:
    """
    Generates captions based on the detected moment using Gemini.
    """
    if not settings.GOOGLE_API_KEY:
        return ["No API Key Caption 1", "No API Key Caption 2"]

    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        tags = ", ".join(moment.get("tags", []))
        mood = moment.get("mood_score", 0.5)

        prompt = (
            f"Generate 3 funny meme captions for an image with these tags: {tags}. "
            f"The mood intensity is {mood}/1.0. "
            "Return ONLY a JSON array of strings used for captions."
        )

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]

        captions = json.loads(text)
        if isinstance(captions, list):
            return captions
        return ["Could not parse captions"]

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return ["Error generating captions", "Check logs"]
