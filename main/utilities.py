from PIL import Image, ImageDraw
import numpy as np
import os
from math import sqrt

def createDottedImage(image_path, num_dots=1000, shape="circle", size=None, shape_color=None, background_color=None):
    bg_rgb = hex_to_rgb(background_color)
    img = Image.open(image_path).convert("RGB")
    img = img.resize((400, 400))
    np_img = np.array(img)

    width, height = img.size
    total_area = width * height
    area_per_dot = total_area / num_dots
    approx_spacing = int(sqrt(area_per_dot))

    # Ensure valid range
    step = max(2, min(20, approx_spacing))

    dot_img = Image.new("RGB", img.size, bg_rgb)
    draw = ImageDraw.Draw(dot_img)

    for y in range(0, height, step):
        for x in range(0, width, step):
            r, g, b = np_img[y][x]
            brightness = int(0.299 * r + 0.587 * g + 0.114 * b)

            if shape_color:
                fill_color = hex_to_rgb(shape_color)
            else:
                fill_color = (r, g, b)

            # Determine radius
            if size is not None:
                radius = size
            else:
                radius = max(1, min(5, step // 3 - brightness // 64))

            left = max(0, x - radius)
            top = max(0, y - radius)
            right = min(width, x + radius)
            bottom = min(height, y + radius)

            if right >= left and bottom >= top:
                if shape == "circle":
                    draw.ellipse((left, top, right, bottom), fill=fill_color)
                elif shape == "square":
                    draw.rectangle((left, top, right, bottom), fill=fill_color)
                elif shape == "triangle":
                    triangle = [(x, top), (left, bottom), (right, bottom)]
                    draw.polygon(triangle, fill=fill_color)

    output_path = image_path.replace("uploads", "dot_art")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dot_img.save(output_path)

    return output_path  


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))