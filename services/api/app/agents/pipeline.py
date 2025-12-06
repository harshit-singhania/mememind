from app.agents import moment_detector, humor_engine, template_stylist

def run_meme_pipeline(media_path: str) -> dict:
    moment = moment_detector.detect_moment(media_path)
    captions = humor_engine.generate_captions(moment)
    final_path = template_stylist.compose_template(captions[0], media_path)
    
    return {
        "status": "completed",
        "result_path": final_path,
        "caption": captions[0]
    }
