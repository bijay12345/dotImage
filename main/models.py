from django.db import models

# Create your models here.

class Art(models.Model):
    original_file = models.ImageField(upload_to="originalFileStorage/")
    converted_art = models.ImageField(upload_to="convertedArtStorage/", null=True)
    creation_type = models.CharField(max_length=20, default="dots")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"