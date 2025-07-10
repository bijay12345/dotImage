from PIL import Image, ImageDraw,ImageEnhance, ImageOps
import numpy as np
import os
from django.conf import settings

class ImageProcessing:
    def __init__(self):
        self.border_thickness = settings.IMAGE_BORDER_THICKNESS
        self.border_color = settings.IMAGE_BORDER_COLOR
        self.standard_height = settings.STANDARD_HEIGHT
        self.standard_width = settings.STANDARD_WIDTH

    def resizeImage(self, file_path=None, size=None, canvas_color = 'white'):
        if(file_path):
            img = Image.open(file_path).convert('RGBA')
            width = self.standard_width if size is None else size[0]
            height = self.standard_height if size is None else size[1]
            img = img.resize((width, height))
            return img
        else:
            width = self.standard_width if size is None else size[0]
            height = self.standard_height if size is None else size[1]
            canvas = Image.new("RGB", (width, height), canvas_color) 
            return canvas
        
    def createDottedImage(self, image_path):
        # Load resize
        img = self.resizeImage(image_path)

        # Brightness enhancement
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.5)  # Increase brightness (1.0 = original, >1 = brighter)

        np_img = np.array(img)

        # Create a blank white image
        dot_img = self.resizeImage()
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

        canvas = self.resizeImage(size=[1024, 1024]) # Creating a blank canvas
        canvas = ImageOps.expand(canvas, border=self.border_thickness, fill=self.border_color)
        img = self.resizeImage(image_path) # resizing and returns a img object.
        if(watermark_text):
            pass
        elif(watermark_image_path): 
            watermark_image = self.resizeImage(watermark_image_path)
            alpha_channel = watermark_image.split()[3]            # Split returns [r,g,b,a] so, getting alpha channel by indexing.
            opacity = 0.3
            alpha = ImageEnhance.Brightness(alpha_channel).enhance(opacity)
            watermark_image.putalpha(alpha)  # Finally assigning the reduced alpha channel to the backgroundImage, this will reduce the image opacity
            img.paste(watermark_image, (0,0), watermark_image)  # Paste the watermark with transparency
        canvas.paste(img, (10,10))  # Add the resized image in the blank canvas
        canvas.show()
        

