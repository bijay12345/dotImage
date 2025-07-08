from PIL import Image, ImageDraw,ImageEnhance
import numpy as np
import os
from math import sqrt
from .enums import ImageTypeEnum

class ImageProcessing:
    def __init__(self):
        pass

    def resizeImage(self, file_path):
        img = Image.open(file_path).convert('RGBA')
        img = img.resize((490, 490))
        return img
    
    def createDottedImage(self, image_path):
        # Load resize
        img = self.resizeImage(image_path)

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
                radius = max(1, 4 - brightness.any() // 64)
 
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


    def createLayeredImage(self,instance):
        image_path = instance.original_file.path
        watermark_text = instance.watermark_text
        watermark_image_path = instance.watermark_image.path if instance.watermark_image else None
        background_image_path = instance.background_image.path if instance.background_image else None 
        canvas = Image.new("RGB", (500,500), (114,35,35)) # Creating a blank canvas
        img = self.resizeImage(image_path)

        if(watermark_text):
            pass
        elif(watermark_image_path):
            watermark_image = self.resizeImage(watermark_image_path)
            alpha = watermark_image.split()[2]
            opacity = 0.3
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark_image.putalpha(alpha)

            # Create a new image for combining
            watermarked = Image.new("RGBA", img.size)
            watermarked.paste(img, (0, 0))

            # Paste the watermark with transparency
            watermarked.paste(watermark_image, (0,0), watermark_image)
        canvas.paste(watermarked, (5,5))  # Add the resized image in the blank canvas
        canvas.show()
        

