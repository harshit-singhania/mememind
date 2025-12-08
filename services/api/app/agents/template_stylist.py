def compose_template(caption: str, image_path: str) -> str:
    """
    Overlays caption on image.
    TODO: Integrate Imaging Lib
    """
    import time
    import textwrap
    from PIL import Image, ImageDraw, ImageFont

    timestamp = int(time.time())
    timestamp = int(time.time())
    output_path = f"/tmp/meme_{timestamp}.jpg"
    
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if needed (e.g. for RGBA/P images to save as JPEG)
            if img.mode != "RGB":
                img = img.convert("RGB")
                
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            # Dynamic font size based on image width
            font_size = int(width / 15)
            font = None
            font_name = "Unknown"
            
            # Try loading common fonts
            font_candidates = [
                "arial.ttf", 
                "Arial.ttf",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            ]
            
            for f_name in font_candidates:
                try:
                    font = ImageFont.truetype(f_name, font_size)
                    font_name = f_name
                    print(f"DEBUG: Loaded font: {f_name}")
                    break
                except IOError:
                    continue
            
            if font is None:
                print("DEBUG: Falling back to default font")
                try:
                    # Pillow 10.1+ supports size param for default font
                    font = ImageFont.load_default(size=font_size)
                except TypeError:
                    # Older Pillow
                    font = ImageFont.load_default()
                    print("DEBUG: Warning - Using tiny default font (Pillow version old?)")

            print(f"DEBUG: Composing meme with caption: '{caption}'")
            print(f"DEBUG: Image size: {width}x{height}")
            print(f"DEBUG: Font size: {font_size}")

            # Layout constants
            padding_x = int(width * 0.05)
            padding_y = int(height * 0.05)
            max_text_width = width - (2 * padding_x)
            
            # Wrap text accurately
            lines = []
            words = caption.upper().split()
            current_line = []
            
            for word in words:
                current_line.append(word)
                # Check width of current line
                test_line = " ".join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]
                
                if line_width > max_text_width:
                    if len(current_line) == 1:
                        # Single word too long, force wrap/split not implemented, just keep it
                        lines.append(current_line[0])
                        current_line = []
                    else:
                        # Pop last word and move to next line
                        current_line.pop()
                        lines.append(" ".join(current_line))
                        current_line = [word]
            
            if current_line:
                lines.append(" ".join(current_line))
                
            print(f"DEBUG: Wrapped lines: {lines}")
            
            # Calculate total text height to center vertically in bottom area or just place closely
            total_text_height = 0
            line_heights = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                h = bbox[3] - bbox[1]
                line_heights.append(h)
                total_text_height += h + 10 # 10px spacing

            # Start drawing from bottom up or top down? Top down from calculated start Y.
            # Position text at the bottom with padding
            y_text = height - total_text_height - padding_y
            
            # If text is too tall, push it up, but don't go off top
            if y_text < padding_y: 
                y_text = padding_y 
            
            print(f"DEBUG: Starting Y position: {y_text}")
            
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                
                x_text = (width - text_width) / 2
                
                # Thick Outline
                outline_color = "black"
                stroke_width = max(2, int(font_size / 10))
                
                # Draw text with outline
                draw.text((x_text, y_text), line, font=font, fill="white", stroke_width=stroke_width, stroke_fill=outline_color)
                
                # Increment Y
                if i < len(line_heights):
                    y_text += line_heights[i] + 10

            img.save(output_path)
            
    except Exception as e:
        print(f"Error composing meme: {e}")
        # Fallback to just copy if image processing fails
        # Fallback to just copy if image processing fails
        import shutil
        import os
        if os.path.exists(image_path):
            shutil.copy(image_path, output_path)
        else:
            print(f"Error: Source file {image_path} not found for fallback.")
            return ""

    return output_path
