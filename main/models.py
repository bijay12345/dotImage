from django.db import models

# Create your models here.

class Art(models.Model):
    original_file = models.ImageField(upload_to="originalFileStorage/")
    dotted_image = models.ImageField(upload_to="convertedArtStorage/", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"