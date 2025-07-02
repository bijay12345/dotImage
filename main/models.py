from django.db import models

# Create your models here.

class Art(models.Model):
    title=models.CharField(max_length=100, null=True)
    description=models.CharField(max_length=300, null=True)
    original_file = models.ImageField(upload_to="originalFileStorage/")
    dotted_image = models.ImageField(upload_to="convertedArtStorage/", null=True)
    shape=models.CharField(max_length=100, null=True)
    size=models.CharField(max_length=100, null=True)
    shape_count=models.IntegerField(null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"