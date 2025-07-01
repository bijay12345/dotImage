from django.shortcuts import render
from main.utilities import createDottedImage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .serializers import ArtSerializer


# Create your views here.
# def index(request):
#     if request.method == "POST":
#         data = request.FILES.get("image")
#         dottedImage = createDottedImage(data)
#         pass
#     return render(request, "main/imageupload.html")


class ArtView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        return render(request, "main/imageupload.html")

    def post(self, request):
        data = request.data
        dots = 10000000000000 # Make it accept from request data in future.
        serializer = ArtSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            # Generate Dot Images
            dot_image = createDottedImage(instance.original_file.path, dots)
            instance.dotted_image.name = dot_image.split('media/')[-1]
            instance.save()

            return Response(ArtSerializer(instance).data)
        return Response(serializer.errors, status=404)