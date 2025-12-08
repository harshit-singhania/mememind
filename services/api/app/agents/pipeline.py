from app.agents import moment_detector, humor_engine, template_stylist
from app.agents.reel_composer import ReelComposer
import asyncio
import time

def run_meme_pipeline(media_path: str) -> dict:
    moment = moment_detector.detect_moment(media_path)
    print(f"DEBUG: Detected moment: {moment}")
    
    captions = humor_engine.generate_captions(moment)
    print(f"DEBUG: Generated captions: {captions}")
    
    final_path = template_stylist.compose_template(captions[0], media_path)
    
    return {
        "status": "completed",
        "result_path": final_path,
        "caption": captions[0]
    }

async def run_video_pipeline(media_path: str) -> dict:
    moment = moment_detector.detect_moment(media_path)
    print(f"DEBUG: Detected moment (Video): {moment}")
    
    captions = humor_engine.generate_captions(moment)
    print(f"DEBUG: Generated captions (Video): {captions}")
    
    # Default high mood if missing
    mood = moment.get('mood_score', 0.5)
    
    composer = ReelComposer(output_dir="/tmp")
    timestamp = int(time.time())
    output_path = f"/tmp/reel_{timestamp}.mp4"
    
    # Run async composer
    final_path = await composer.generate_reel(media_path, captions[0], mood, output_path)
    
    return {
        "status": "completed",
        "result_path": final_path,
        "caption": captions[0]
    }
