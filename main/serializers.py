from rest_framework import serializers
from .models import Art

class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields=["id", "title", "description","original_file", "shape", "size","shape_count","dotted_image","uploaded_at"]
        extra_kwargs = {'dot_image': {'reaad_only': True}}