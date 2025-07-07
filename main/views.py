from django.shortcuts import render
from main.utilities import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .serializers import ArtSerializer
from django.shortcuts import redirect
from .enums import ImageTypeEnum
from .utilities import ImageProcessing

class ArtView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return render(request, "main/imageupload.html")

    def post(self, request):
        data = request.data
        serializer = ArtSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            # Generate custom Images
            imageProcessor = ImageProcessing()
            if(instance.creation_type == ImageTypeEnum.DOTTED.value):
                processed_image = imageProcessor.createDottedImage(instance.original_file.path)
            elif(instance.creation_type == ImageTypeEnum.LAYERED.value):
                processed_image = imageProcessor.createLayeredImage(instance.original_file.path)
            else:
                return Response("Not a valid option", 402)
            instance.converted_art.name = processed_image.split('media/')[-1]
            instance.save()

            return redirect("/")
        return Response(serializer.errors, status=404)