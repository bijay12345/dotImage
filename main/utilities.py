from PIL import Image, ImageDraw
import numpy as np
import os
from math import sqrt

def createDottedImage(image_path, num_dots=10000):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((400, 400))  # Resize for uniform density (optional)
    np_img = np.array(img)

    width, height = img.size
    total_area = width * height
    area_per_dot = total_area / num_dots
    approx_spacing = int(sqrt(area_per_dot))  # Approximate step size

    # Ensure valid range
    step = max(2, min(20, approx_spacing))

    dot_img = Image.new("RGB", img.size, "white")
    draw = ImageDraw.Draw(dot_img)

    for y in range(0, height, step):
        for x in range(0, width, step):
            r,g,b = np_img[y][x]
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b) 
            
            radius = max(1, min(5, step // 3 - brightness // 64))

            left = max(0, x - radius)
            top = max(0, y - radius)
            right = min(width, x + radius)
            bottom = min(height, y + radius)

            if right >= left and bottom >= top:
                draw.ellipse((left, top, right, bottom), fill=(r,g,b))

    output_path = image_path.replace("uploads", "dot_art")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dot_img.save(output_path)

    return output_path