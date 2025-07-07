from PIL import Image, ImageDraw,ImageEnhance
import numpy as np
import os
from math import sqrt

def createDottedImage(image_path, num_dots=10000):
    # Load, convert to grayscale, and resize
    img = Image.open(image_path).convert("L")
    img = img.resize((200, 200))

    # Brightness enhancement
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.5)  # Increase brightness (1.0 = original, >1 = brighter)

    np_img = np.array(img)

    # Create a blank white image
    dot_img = Image.new("RGB", img.size, "white")
    draw = ImageDraw.Draw(dot_img)

    step = 3  # More dots

    for y in range(0, img.size[1], step):
        for x in range(0, img.size[0], step):
            brightness = np_img[y][x]

            # Smaller dots in brighter areas
            radius = max(1, 4 - brightness // 64)

            x0 = x - radius
            y0 = y - radius
            x1 = x + radius
            y1 = y + radius

            x0 = max(0, x0)
            y0 = max(0, y0)
            x1 = min(img.size[0] - 1, x1)
            y1 = min(img.size[1] - 1, y1)

            if x1 >= x0 and y1 >= y0:
                draw.ellipse((x0, y0, x1, y1), fill="black")

    output_path = image_path.replace("uploads", "dot_art")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dot_img.save(output_path)

    return output_path
