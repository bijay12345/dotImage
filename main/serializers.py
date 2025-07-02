from rest_framework import serializers
from .models import Art

class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields=['id',"original_file","dotted_image","uploaded_at"]
        extra_kwargs = {'dot_image': {'reaad_only': True}}