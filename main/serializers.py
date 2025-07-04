from rest_framework import serializers
from .models import Art
import re

class ColorField(serializers.CharField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not re.match(r'^#([A-Fa-f0-9]{6})$', data):
            raise serializers.ValidationError("Invalid color code")
        return data

class ArtSerializer(serializers.ModelSerializer):
    shape_color = ColorField(write_only=True, required=False,default="#fcb603")
    class Meta:
        model = Art
        fields=["id", "title", "description","original_file",
                 "shape", "size","shape_count", "shape_color", "background_color","dotted_image","uploaded_at"]
        extra_kwargs = {'dot_image': {'read_only': True}}