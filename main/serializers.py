from rest_framework import serializers
from .models import Art

class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Art
        fields="__all__"