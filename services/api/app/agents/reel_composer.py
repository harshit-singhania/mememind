import os
import random
import asyncio
from moviepy import *
import edge_tts
from app.core.config import settings

class ReelComposer:
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = output_dir
        self.music_dir = os.path.join(os.getcwd(), "app/static/music")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.music_dir, exist_ok=True)

    async def generate_reel(self, image_path: str, caption: str, mood_score: float, output_path: str) -> str:
        """
        Generates a video reel from an image and caption.
        """
        try:
            print(f"DEBUG: Starting Reel Generation for {image_path}")
            
            # 1. Generate Audio (TTS)
            tts_path = os.path.join(self.output_dir, f"tts_{os.path.basename(image_path)}.mp3")
            await self._generate_tts(caption, tts_path)
            
            if not os.path.exists(tts_path) or os.path.getsize(tts_path) == 0:
                 print("ERROR: TTS generation failed (Empty or missing file)")
                 return ""
            
            print(f"DEBUG: TTS generated successfully. Size: {os.path.getsize(tts_path)} bytes")

            # 2. Generate Text Overlay Frame
            from app.agents import template_stylist
            # We need dimensions. Open image temporarily (MoviePy will reopen it but that's fine)
            from PIL import Image
            with Image.open(image_path) as img:
                w, h = img.size
            
            # Ensure Even Dimensions (Important for H.264/Mobile)
            if w % 2 != 0: w -= 1
            if h % 2 != 0: h -= 1
            
            overlay_path = template_stylist.create_text_overlay(caption, w, h)
            if not overlay_path:
                print("ERROR: Overlay generation failed")
                return ""

            # 3. Create Video Layout
            # Duration: TTS length + 1.5s padding
            tts_clip = AudioFileClip(tts_path)
            video_duration = tts_clip.duration + 1.5
            
            # Base Image with Zoom (Ken Burns)
            # v2 uses methods on clip usually, or vfx
            # Standard simple zoom: resize over time
            # 1.0 at output, to 1.1x
            
            # Note: For simple "Ken Burns", we crop a larger image.
            # But let's keep it simple: Resize starts at 1.0, grows to 1.1
            # We need to set_position('center') so it grows from middle
            
            img_clip = ImageClip(image_path).with_duration(video_duration)
            
            # Apply zoom: t=0 -> 1.0, t=duration -> 1.15
            # NOTE: In MoviePy v2, vfx.Resize might not be directly importable as `vfx`.
            # We used `from moviepy import *`. `vfx` usually available if we modify imports or use `msg.vfx`.
            # Let's verify imports first or use specific Transform.
            
            # Safest approach for MoviePy 1.x/2.x mixed docs:
            # clip.resize(lambda t: 1 + 0.02 * t)
            
            # But `resize` is often an effect.
            # Let's try the method approach which is cleaner in updated moviepy
            zoom_clip = img_clip.with_effects([vfx.Resize(lambda t: 1 + 0.05 * t)])
            zoom_clip = zoom_clip.with_position('center')

            # Text Overlay (Static on top)
            txt_clip = ImageClip(overlay_path).with_duration(video_duration)
            
            # 4. Composite
            video = CompositeVideoClip([zoom_clip, txt_clip], size=(w,h))
            
            # 5. Audio
            # Mix TTS + Background Music (if any)
            # For now, just TTS
            video = video.with_audio(tts_clip)
            
            # 6. Write File
            # preset='ultrafast' for dev speed
            # -pix_fmt yuv420p is CRITICAL for mobile (Android/iOS) compatibility
            video.write_videofile(
                output_path, 
                codec="libx264", 
                fps=24, 
                preset="ultrafast", 
                audio_codec="aac",
                ffmpeg_params=["-pix_fmt", "yuv420p"]
            )
            
            print(f"DEBUG: Reel generated at {output_path}")
            
            # Cleanup temps
            try:
                os.remove(tts_path)
                os.remove(overlay_path)
            except:
                pass
                
            return output_path

        except Exception as e:
            print(f"Error generating reel: {e}")
            import traceback
            traceback.print_exc()
            return ""

    async def _generate_tts(self, text: str, output_path: str):
        """
        Generates TTS audio using edge-tts, falling back to gTTS.
        """
        # Clean text
        clean_text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
        
        try:
            # Randomize voice slightly? Or stick to a good one.
            voice = "en-US-GuyNeural" # Standard male voice, often more reliable
            communicate = edge_tts.Communicate(clean_text, voice)
            await communicate.save(output_path)
            
            # Verify it actually wrote data
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise Exception("edge-tts produced empty file")
                
            print(f"DEBUG: TTS saved to {output_path} (edge-tts)")
            
        except Exception as e:
            print(f"Warning: edge-tts failed ({e}). Falling back to gTTS...")
            try:
                from gtts import gTTS
                # gTTS is synchronous, run in thread or just block (short text is fast)
                tts = gTTS(clean_text, lang='en')
                tts.save(output_path)
                print(f"DEBUG: TTS saved to {output_path} (gTTS)")
            except Exception as e2:
                print(f"Error in TTS generation (all methods failed): {e2}")

    def _select_bg_music(self, mood_score: float) -> str:
        """
        Selects a background track based on mood.
        """
        # TODO: Implement actual selection logic
        return None
